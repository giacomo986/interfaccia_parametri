import boto3

s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
    print(bucket.name)

#App.ActiveDocument.saveAs("/home/giacomo/test_freecad/prova.FCStd")

data = open("/home/giacomo/test_freecad/prova.FCStd", 'rb')
s3.Bucket('disegni.freecad').put_object(Key='prova.FCStd', Body=data)
