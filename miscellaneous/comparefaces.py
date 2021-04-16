import boto3

BUCKET = "frame-s3-proj"
KEY_SOURCE = "frames/2018/09/11/11/4e4cfe6f-23ee-4381-8e8b-53c3f45a5d33.jpg"
KEY_TARGET = "frames/2018/09/11/11/4e4cfe6f-23ee-4381-8e8b-53c3f45a5d33.jpg"


def compare_faces(bucket, key, bucket_target, key_target, threshold=80, region="us-east-1"):
    rekognition = boto3.client("rekognition", region)
    response = rekognition.compare_faces(
        SourceImage={
            "S3Object": {
                "Bucket": bucket,
                "Name": key,
            }
        },
        TargetImage={
            "S3Object": {
                "Bucket": bucket_target,
                "Name": key_target,
            }
        },
        SimilarityThreshold=threshold,
    )
    return response['SourceImageFace'], response['FaceMatches']


source_face, matches = compare_faces(BUCKET, KEY_SOURCE, BUCKET, KEY_TARGET)

# the main source face
print( "Source Face ({Confidence}%)".format(**source_face))

# one match for each target face
for match in matches:
    print("Target Face ({Confidence}%)".format(**match['Face']))
    print("  Similarity : {}%".format(match['Similarity']))
