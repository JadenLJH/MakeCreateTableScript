import pandas as pd
import math

# 엑셀 파일 경로 설정
excel_path = 'DataBase Table.xlsx'

# 엑셀 파일 로드
xls = pd.ExcelFile(excel_path)

def sql_type_map(excel_dtype):
    # Excel 데이터 타입을 SQL 데이터 타입으로 매핑하는 간단한 함수
    return excel_dtype  # 복잡한 매핑이 필요할 경우 이 부분을 조정

def generate_sql(table_name, df):
    sql_columns = []
    primary_key = ''
    foreign_keys = []
    
    for _, row in df.iterrows():
        column_name = row['열이름']
        data_type = sql_type_map(row['데이터 타입'])
        constraints = []
        default = row.get('DEFAULT', '')
        
        if row['AUTO_INCREMENT'] == 'YES':
            constraints.append(' AUTO_INCREMENT')
        if row['PK'] == 'YES':
            constraints.append(' PRIMARY KEY')
        if row['UNIQUE'] == 'YES':
            constraints.append(' UNIQUE')
        if row['NOT_NULL'] == 'YES':
            constraints.append(' NOT NULL')
        if math.isnan( default) == False:
            constraints.append(f" DEFAULT {default}")
        if pd.notna(row['FK']) and pd.notna(row['FK 참조 테이블']):
            constraints.append(f" REFERENCES {row['FK 참조 테이블']}({column_name})")
        
        column_definition = f"{column_name} {data_type}"
        for constraint in constraints:
            column_definition += constraint
        sql_columns.append(column_definition)
    
    sql_script = f"CREATE TABLE {table_name} (\n"
    sql_script += ",\n".join(sql_columns)
    sql_script += "\n);"
    
    return sql_script

# 모든 시트를 반복하며 SQL 스크립트 생성
for sheet_name in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name)
    sql_script = generate_sql(sheet_name, df)
    print(f"-- {sheet_name} Table Creation Script --")
    print(sql_script)
    print("\n")

input()