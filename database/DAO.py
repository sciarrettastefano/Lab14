from database.DB_connect import DBConnect
from model.order import Order
from model.store import Store


class DAO():

    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from stores"""

        cursor.execute(query)

        for row in cursor:
            result.append(Store(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllOrders(storeId):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from orders
                    where store_id = %s"""

        cursor.execute(query, (storeId,))

        for row in cursor:
            result.append(Order(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(k, storeId, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT distinct o.order_id as id1, o2.order_id as id2, count(oi.quantity + oi2.quantity) as peso
                    from orders o, orders o2, order_items oi, order_items oi2 
                    where o.order_id > o2.order_id
                    and o.order_id = oi.order_id
                    and o2.order_id = oi2.order_id
                    and o.order_date > o2.order_date
                    and DATEDIFF(o.order_date, o2.order_date) < %s
                    and o.store_id = o2.store_id
                    and o.store_id = %s
                    group by id1, id2"""

        cursor.execute(query, (k, storeId,))

        for row in cursor:
            result.append((idMap[row["id1"]], idMap[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return result


