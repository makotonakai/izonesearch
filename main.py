
from flask import *
from PIL import Image
import os
import glob
import random
import psycopg2

app = Flask(__name__)

# 最初の画面
@app.route('/', methods=["GET"])
def index():

    return render_template("index.html")



@app.route('/index', methods=["POST"])
def post():

    for file in glob.glob('./static/pics/*.jpg'):
        os.remove(file)

    # 選んだメンバーの名前を取得
    name = request.form.get("name")
    num_pics = int(request.form.get("num_pics"))
    print(name)
    print(num_pics)


    select_name = []
    value_list = ["Kwon_Eunbi", "Sakura_Miyawaki", "Hyewon_Kang", "Yena_Choi", "Cheyeon_Lee", \
                "Chewon_Kim", "Minju_Kim", "Nako_Yabuki", "Hitomi_Honda", "Yuri_Choi", "Yujin_Ahn", "Wonyoung_Chang"]
    name_list = ["Kwon Eunbi", "Sakura Miyawaki", "Hyewon Kang", "Yena Choi", "Cheyeon Lee", \
                "Chewon Kim", "Minju Kim", "Nako Yabuki", "Hitomi Honda", "Yuri Choi", "Yujin Ahn", "Wonyoung hang"]

    for num in range(len(value_list)):
        if name_list[num] == name:
            select_name.append('<option value="{}" selected> {} </option>'.format(value_list[num], name_list[num]))
        else:
            select_name.append('<option value="{}"> {} </option>'.format(value_list[num], name_list[num]))


    select_num_pics = []
    num_pics_list = [1, 5, 10, 20]

    for idx in range(len(num_pics_list)):
        if num_pics_list[idx] == num_pics:
            select_num_pics.append('<option value='+str(num_pics_list[idx])+'selected>'+str(num_pics_list[idx])+'</option>')
        else:
            select_num_pics.append('<option value='+str(num_pics_list[idx])+'>'+str(num_pics_list[idx])+'</option>')


    file_list = []

    id_list = [random.randint(0, 40) for i in range(num_pics)]
    for id_ in id_list:
    
        query = "SELECT * FROM izonetable WHERE member = %s AND id = %s"
        filename = "./static/pics/pic_{}.jpg".format(id_)

        DATABASE_URL = "postgres://youylcnkjyfyfy:20a5d945df5a9da524c823962294428191105ef78735d82ff42d3ba216642a5b@ec2-50-16-198-4.compute-1.amazonaws.com:5432/d8o6aq59fi4v03"
        connect = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connect.cursor() 

        try:
            cursor.execute(query, (name, id_))
            fetch = cursor.fetchone()
            
            image = fetch[2]

            with open(filename, 'wb') as f:
                f.write(bytes(image))
            file_list.append(filename)

        except Exception as e:
            print(e)

        finally:
            cursor.close()
            connect.close()

    return render_template("result.html", select_name=select_name, select_num_pics=select_num_pics, file_list=file_list)



if __name__ == "__main__":
    app.run(debug=True, threaded=True)


    
