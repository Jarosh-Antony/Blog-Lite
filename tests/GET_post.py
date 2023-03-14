def result_GET_Post():
    result=[]
    
    login_credential={"Authorization":"WyJhODI4ODEzM2EzZDI0ZThkODJlNzlhZGVmZmU5NDdmZSJd.ZA4X5Q.IDrNhmdrrNuO6nnOLGyYyb4c9vo"}
    json_response={
                    "posts": [
                        {
                            "id": 6,
                            "title": "post1",
                            "description": "this is my post 1 by jarosh",
                            "timestamp": "2023-03-08 13:09:03.858694",
                            "imageurl": "..\\post_images\\1_2023-03-08-13-09-03-858694_Snapshot_245.png"
                        },
                        {
                            "id": 7,
                            "title": "post2",
                            "description": "this is my post 2 by jarosh",
                            "timestamp": "2023-03-08 13:09:40.227679",
                            "imageurl": "..\\post_images\\1_2023-03-08-13-09-40-227679_Snapshot_241.png"
                        },
                        {
                            "id": 8,
                            "title": "post1",
                            "description": "this is my post 1 by thomas",
                            "timestamp": "2023-03-08 13:10:46.917875",
                            "imageurl": "..\\post_images\\2_2023-03-08-13-10-46-917875_Snapshot_243.png"
                        }
                    ]
                }
    
    test=(login_credential,json_response)
    result.append(test)
    
    login_credential={"Authorization":"WyI0OWFlMGRiMmU0YmI0NzI4Yjc1MDk5Y2Y3ZDIzNzUwNSJd.ZA4YNA.3h4-ZKPIFh6VSOlVNEnOg5U7R84"}
    json_response={
                    "posts": [
                    ]
                }
    
    test=(login_credential,json_response)
    result.append(test)
    
    return result