import pymysql
import xlwt
import datetime

if __name__ == '__main__':
    keys = ['澳门', '澳', '粤', '广东', '珠三角', '珠江三角洲', '粤港澳大湾区', '粤港澳', '大湾区', '广州', '深圳', '珠海', '佛山',
            '惠州', '东莞', '中山', '江门', '肇庆', '孙中山', '中山先生']
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day

    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456',
                                db='news', charset='utf8')
    cursor = conn.cursor()

    twb = xlwt.Workbook()
    tst = twb.add_sheet('sheet1')
    tst.write(0, 0, '时间')
    for i in range(len(keys)):
        tst.write(0, i + 1, keys[i])
    tst.write(0, 21, '空缺天日期')

    count = 0
    for i in range(2012, year + 1):
        for j in range(1, 13):
            if i == year and j > month:
                break
            count += 1
            wb = xlwt.Workbook()
            st = wb.add_sheet('sheet1')
            st.write(0, 0, '标题')
            st.write(0, 1, '时间')
            y = str(i)
            m = '0' + str(j) if j < 10 else str(j)
            filename = y + '-' + m
            lack = []
            news = []
            key_dt = dict()
            for key in keys:
                key_dt[key] = 0
            for k in range(1, 32):
                if i == year and j == month and k > day:
                    break
                if i % 4 == 0:
                    if j == 2 and k > 29:
                        break
                else:
                    if j == 2 and k > 28:
                        break
                if j % 2 != 0 and k > 30:
                    break
                d = '0' + str(k) if k < 10 else str(k)
                t = y + '-' + m + '-' + d
                sql = '''select distinct(title) from news where publish_date = '%s' ''' % t
                cursor.execute(sql)
                rs = cursor.fetchall()
                if len(rs) == 0:
                    lack.append(str(k))
                for item in rs:
                    for key in keys:
                        if key in item[0]:
                            key_dt[key] += 1
                    news.append((item[0], t))
            for x in range(len(news)):
                st.write(x + 1, 0, news[x][0])
                st.write(x + 1, 1, news[x][1])
            wb.save('./data/' + filename + '.xls')
            tst.write(count, 0, filename)
            for x in range(len(keys)):
                tst.write(count, x + 1, key_dt[keys[x]])
            tst.write(count, 21, ','.join(lack))
    twb.save('total.xls')
