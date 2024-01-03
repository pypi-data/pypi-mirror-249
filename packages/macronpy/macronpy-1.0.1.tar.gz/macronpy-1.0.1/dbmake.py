import sqlite3
import os

wds_dir=r"D:\Users\niupeiyi\资产配置研究\market_data\wind"
fund_dir=r"D:\Users\niupeiyi\资产配置研究\market_data\windcustom\fund"
#【NOTE】最多10个数据库！超出python会报错。所以把fund里面的数据库拆开来，放一个fund2
fund2_dir=r"D:\Users\niupeiyi\资产配置研究\market_data\windcustom\fund2"
hshare_dir=r"D:\Users\niupeiyi\资产配置研究\market_data\windcustom\hshare"

def initial_db(cd):
    '''
    根据传入的路径，生成数据库合集
    '''
    # try:
    #     # 获取文件夹中的所有数据库文件
    #     db_files = [file for file in os.listdir(cd) if file.endswith(".db")]
    #     # 创建连接
    #     db = sqlite3.connect(os.path.join(cd, db_files[0]))
    #     # 依次附加数据库文件到连接
    #     # for db_file in db_files[1:]:
    #     for db_file in db_files:
    #         print(db_file)
    #         db_path = os.path.join(cd, db_file)
    #         db.execute(f"ATTACH DATABASE '{db_path}' AS '{db_file[:-3]}'")
    # except:
    #     print("")
    # 获取文件夹中的所有数据库文件
    db_files = [file for file in os.listdir(cd) if file.endswith(".db")]
    # 创建连接
    db = sqlite3.connect(os.path.join(cd, db_files[0]))
    # 依次附加数据库文件到连接
    # for db_file in db_files[1:]:
    for db_file in db_files:
        # print(db_file)
        db_path = os.path.join(cd, db_file)
        db.execute(f"ATTACH DATABASE '{db_path}' AS '{db_file[:-3]}'")
    return db

#生成数据库链接的全局变量
wds=initial_db(wds_dir)
fundb=initial_db(fund_dir)
fundb2=initial_db(fund2_dir)
hshare=initial_db(hshare_dir)


