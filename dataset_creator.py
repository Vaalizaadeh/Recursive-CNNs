import os
import cv2
import xml.etree.ElementTree as ET
import random
w = 150
h = 150

def get_cords(cord, min_start, max_end, size = 299 , buf = 0, random_scale=True):
    #size = max(abs(cord-min_start), abs(cord-max_end))
    iter=0
    if(random_scale):
        size/= random.randint(1,4) 
    while(max_end - min_start)<size:
        size=size*.9
    x_start = random.randint(min(max(min_start, cord-size+buf), cord-buf-1), cord-buf)
    while(x_start+size> max_end):
        x_start = random.randint(min(max(min_start,int(cord - size + buf)),cord-buf-1), cord - buf)
        size=size*.999
        iter+=1
        if(iter==1000):
            x_start= min_start
            break 
    return (x_start, int(x_start+size))

if __name__ == '__main__':
    dir = "."
    import csv

    with open('gt1.csv', 'a') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for folder in os.listdir(dir):
            if(os.path.isdir(folder)):
                for file in os.listdir(folder):
                    images_dir= dir+"/"+folder+"/"+file
                    if(os.path.isdir(images_dir)):
                        list_gt = []
                        tree = ET.parse(images_dir+"/"+file+".gt")
                        root = tree.getroot()
                        for a in root.iter("frame"):
                            list_gt.append(a)

                        print list_gt
                        for image in os.listdir(images_dir):
                            if image.endswith(".jpg"):
                                try:
                                    #Now we have opened the file and GT. Write code to create multiple files and scale gt
                                    list_of_points = {}
                                    img = cv2.imread(images_dir+"/"+image)
                                    print image[0:-4]
                                    for point in list_gt[int(float(image[0:-4]))-1].iter("point"):
                                        myDict = point.attrib

                                        list_of_points[myDict["name"]] = (int(float(myDict['x'])), int(float(myDict['y'])))
                                    299

                                    doc_height = min(list_of_points["bl"][1] - list_of_points["tl"][1], list_of_points["br"][1] - list_of_points["tr"][1])
                                    doc_width = min(list_of_points["br"][0] - list_of_points["bl"][0], list_of_points["tr"][0] - list_of_points["tl"][0])
                                #  print doc_height
                                #  print doc_height
                                #  print doc_width
                                    import random
                                    for k,v in list_of_points.iteritems():

                                        if(k=="tl"):

                                            cords_x = get_cords(v[0], 0,list_of_points["tr"][0], buf =10, size=abs(list_of_points["tr"][0]-v[0]))
                                            cords_y = get_cords(v[1], 0,list_of_points["bl"][1],buf=10, size=abs(list_of_points["bl"][1]-v[1]))
                                        #    print cords_y, cords_x
                                            gt= (v[0] - cords_x[0], v[1] - cords_y[0])

                                            cut_image = img[cords_y[0]:cords_y[1], cords_x[0]:cords_x[1]]



                                        if (k == "tr"):
                                            cords_x = get_cords(v[0], list_of_points["tl"][0], img.shape[1], buf=10, size=abs(list_of_points["tl"][0]-v[0]))
                                            cords_y = get_cords(v[1], 0, list_of_points["br"][1], buf=10, size=abs(list_of_points["br"][1]-v[1]))
                                        #   print cords_y, cords_x
                                            gt = (v[0] - cords_x[0], v[1] - cords_y[0])

                                            cut_image = img[cords_y[0]:cords_y[1], cords_x[0]:cords_x[1]]


                                        if (k == "bl"):
                                            cords_x = get_cords(v[0], 0, list_of_points["br"][0], buf=10,
                                                                                                size=abs(list_of_points["br"][0] - v[0]))
                                            cords_y = get_cords(v[1], list_of_points["tl"][1], img.shape[0], buf=10,
                                                                size=abs(list_of_points["tl"][1] - v[1]))
                                        #    print cords_y, cords_x
                                            gt = (v[0] - cords_x[0], v[1] - cords_y[0])

                                            cut_image = img[cords_y[0]:cords_y[1], cords_x[0]:cords_x[1]]

                                        if (k == "br"):
                                            cords_x = get_cords(v[0], list_of_points["bl"][0], img.shape[1], buf=10,
                                                                size=abs(list_of_points["bl"][0] - v[0]))
                                            cords_y = get_cords(v[1], list_of_points["tr"][1],img.shape[0], buf=10,
                                                                size=abs(list_of_points["tr"][1] - v[1]))
                                            #print cords_y, cords_x
                                            gt = (v[0] - cords_x[0], v[1] - cords_y[0])

                                            cut_image = img[cords_y[0]:cords_y[1], cords_x[0]:cords_x[1]]

                                        #cv2.circle(cut_image, gt, 2, (255, 0, 0), 6)
                                        mah_size = cut_image.shape
                                        cut_image = cv2.resize(cut_image, (300,300))
                                        a = int(gt[0]*300/mah_size[1])
                                        b = int(gt[1]*300/mah_size[0])
                                    
                                  
                                        cv2.imwrite("../data_set/"+folder+file+image+k+".jpg", cut_image)
                                        spamwriter.writerow((folder+file+image+k+".jpg",(a,b)))
                                except KeyboardInterrupt:
                                    raise
                                except:
                                    print("Exception occured; skipping this image")
                                            # if (k == "tl"):
                                    #     cords_x = get_cords(v[0], 0, list_of_points["tr"][0], 10)
                                    #     cords_y = get_cords(v[1], 0, list_of_points["bl"][1], 10)
                                    #
                                    #     gt = (v[0] - cords_x[0], v[1] - cords_y[0])tf.sq
                                    #
                                    #     cut_image = img[cords_y[0]:cords_y[1], cords_x[0]:cords_x[1]]
                                    #
                                    # if (k == "tl"):
                                    #     cords_x = get_cords(v[0], 0, list_of_points["tr"][0], 10)
                                    #     cords_y = get_cords(v[1], 0, list_of_points["bl"][1], 10)tf.sq
                                    #
                                    #     gt = (v[0] - cords_x[0], v[1] - cords_y[0])
                                    #
                                    #     cut_image = img[cords_y[0]:cords_y[1], cords_x[0]:cords_x[1]]

                                #     start_x = max(0, v[0] - random.randint(1, v[0]))
                                #     end_x = min(img.shape[1], v[0]+random.randint(1,img.shape[1]-v[0]))
                                #     0/0
                                # cv2.imshow("asd", img[max(list_of_points['tl'][1] - doc_height / 2, 0):list_of_points['tl'][1] + doc_height / 2, max(list_of_points['tl'][0] - doc_width / 2, 0):list_of_points['tl'][0] + doc_width / 2, ...])
                                # cv2.waitKey(1)
