import csv
import os


def search(dirname, wr):
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                search(full_filename, wr)
            else:
                ext = os.path.splitext(full_filename)[-1]
                if ext == '.jpg':
                    temp = full_filename.split("/")
                    temp = temp[-1].split("_")
                    #print(temp)
                    angle = temp[0]
                    #temp2 = temp[4].split(".")
                    speed = temp[1]
                    wr.writerow([full_filename,angle,speed])
    except PermissionError:
        pass


if __name__=="__main__":

    file_name = 'output.csv'
    search_dir = "./Image"

    f = open(file_name, 'w', newline='')
    wr = csv.writer(f)

    search(search_dir, wr)          # 전역변수 <-- 이미지폴더 있는 상위 폴더 주소 ex) D:\DeepLearning\2018-05-12 니까 D:/DeepLearning
                                        # Tools - Preferences - current working directory 값 잡아준대에 csv파일 저장됨..
    f.close()
