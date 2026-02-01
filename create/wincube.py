import pandas as pd
import json
from sqlalchemy import create_engine

# 1. JSON 파일 로드
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 설정 정보 변수 할당
db_cfg = config['database']
ex_cfg = config['excel']

# 2. 엑셀 파일 읽기
df = pd.read_excel(ex_cfg['file_path'], sheet_name=ex_cfg['sheet_name'])

# 3. 데이터베이스 연결 (SQLAlchemy)
# f-string을 사용하여 JSON에서 가져온 정보를 조합합니다.
engine_url = f"mysql+pymysql://{db_cfg['user']}:{db_cfg['password']}@{db_cfg['host']}:{db_cfg['port']}/{db_cfg['db_name']}"
engine = create_engine(engine_url)

# 4. DB 테이블로 저장
try:
    df.to_sql(
        name=ex_cfg['table_name'],
        con=engine,
        if_exists='replace',
        index=False
    )
    print(f"✅ 성공: '{ex_cfg['table_name']}' 테이블이 생성되었습니다.")
except Exception as e:
    print(f"❌ 오류 발생: {e}")