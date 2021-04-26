# Exercise

In this exercise we have refactored Barky code to use TDD, Domain model, Repository model and Service layer.
Here we are simulating Bookmark Manager. We should be able to create APIs to perform CRUD operations on bookmarks table 

## How to call different APIs

###List all Bookmarks

curl http://localhost:5000/bookmarks

```
[
  {
    "date_added": "2021-04-02 06:29:43.252057",
    "id": "86bd33e1-c0ef-4ced-b1bf-bda9e6a1029e",
    "notes": "test2 notes",
    "title": "test2",
    "url": "http://test2.com"
  },
  {
    "date_added": "2021-04-02 06:29:43.254656",
    "id": "92c9f229-32fd-4aef-b554-ae971f35842c",
    "notes": "test1 notes",
    "title": "test1",
    "url": "http://test1.com"
  },
  {
    "date_added": "2021-04-02 06:46:49.966311+00:00",
    "id": "b5e56c21-0f8f-4105-a703-edb5b0cdadc4",
    "notes": "test5 notes",
    "title": "test5",
    "url": "http://test5.com"
  }
]

```

###List a Bookmark by ID 

curl http://localhost:5000/bookmarks/92c9f229-32fd-4aef-b554-ae971f35842c/

```
{
  "date_added": "2021-04-02 06:29:43.254656",
  "id": "92c9f229-32fd-4aef-b554-ae971f35842c",
  "notes": "test1 notes",
  "title": "test1",
  "url": "http://test1.com"
}

```




###Insert a Bookmark

curl -vX POST http://localhost:5000/bookmarks/ -d @a.json --header "Content-Type: application/json"


```
create a.json
          {
                              "notes": "test1 notes",
                                  "title": "test1",
                                      "url": "http://test1.com"
                                        }

```



###Update a Bookmark


curl -vX POST http://localhost:5000/bookmarks/b5e56c21-0f8f-4105-a703-edb5b0cdadc4 -d @a.json --header "Content-Type: application/json"


```
create a.json
          {
                              "notes": "test5 notes",
                                  "title": "test5",
                                      "url": "http://test5.com"
                                        }

```


###Delete a Bookmark

 curl -X DELETE http://localhost:5000/bookmarks/b5e56c21-0f8f-4105-a703-edb5b0cdadc4/
