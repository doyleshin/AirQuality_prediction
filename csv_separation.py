from commons import *

def data_separation():
    print('Operating data separation module.')
    with open('160920_sensor.csv', 'r') as csvfile:
        sensor_data = csv.reader(csvfile, quotechar='"')
        i = 0
        for row in sensor_data:
            id = '160921_sensor'
            # Check header & separator
            # About 32,650,000 Lines
            if(i==0):
                header_list = row
            else:
                # id, time, user, serial, value, ip, type, user2
                separator = str(row[2])
                id = id + separator + '.csv'
            i += 1

            # open and write 'row'
            writer = ''
            try:
                f = open(id, 'a', newline='')
                writer = csv.DictWriter(f, fieldnames=header_list)
            except FileNotFoundError:
                print(separator + ' ip generated.')
                f = open(id, 'w+', newline='')
                writer = csv.DictWriter(f, fieldnames=header_list)
                writer.writeheader()
            writer.writerow({'id': row[0], 'time': row[1], 'user': row[2],
                             'serial': row[3], 'value': row[4], 'ip': row[5],
                             'type': row[6],'user2': row[7]})
            f.close()
            if(i%10000 == 0):
                print('%.2f%% is done.' % (float(i)/32650000))
    return 1

if __name__ == "__main__":
    print ('This program is being run by it self.')
    # data_separation()
else:
    print('This program being imported from another module.')