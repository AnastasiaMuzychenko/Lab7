from db import cursor


def query_critical_errors():
    cursor.execute(
        """
    SELECT * FROM Errors WHERE error_level = 'Критична' ORDER BY error_id;
    """
    )
    return cursor.description, cursor.fetchall()


def query_error_levels():
    cursor.execute(
        """
    SELECT error_level, COUNT(*) AS count FROM Errors GROUP BY error_level;
    """
    )
    return cursor.description, cursor.fetchall()


def query_fix_costs():
    cursor.execute(
        """
    SELECT f.fix_id, f.error_id, f.programmer_id, f.duration, f.daily_rate,
           (f.duration * f.daily_rate) AS total_cost
    FROM Fixes f;
    """
    )
    return cursor.description, cursor.fetchall()


def query_errors_by_source(source):
    cursor.execute(
        """
    SELECT * FROM Errors WHERE source = %s;
    """,
        (source,),
    )
    return cursor.description, cursor.fetchall()


def query_errors_by_users_and_testers():
    cursor.execute(
        """
    SELECT source, COUNT(*) AS count FROM Errors WHERE source IN ('Користувач', 'Тестувальник') GROUP BY source;
    """
    )
    return cursor.description, cursor.fetchall()


def query_programmer_error_levels():
    cursor.execute(
        """
    SELECT f.programmer_id,
           SUM(CASE WHEN e.error_level = 'Критична' THEN 1 ELSE 0 END) AS critical,
           SUM(CASE WHEN e.error_level = 'Важлива' THEN 1 ELSE 0 END) AS important,
           SUM(CASE WHEN e.error_level = 'Незначна' THEN 1 ELSE 0 END) AS minor
    FROM Fixes f
    JOIN Errors e ON f.error_id = e.error_id
    GROUP BY f.programmer_id;
    """
    )
    return cursor.description, cursor.fetchall()
