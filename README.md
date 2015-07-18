# Vendor API

:octocat: &nbsp;**Live Site**: <http://vendor-server.herokuapp.com> 

## Endpoints
Articles are stored out by region 
e.g. `nigeria`

### GET all articles
`vendor-server.herokuapp.com/regions/<region>/articles`

### GET trending articles
`vendor-server.herokuapp.com/regions/<region>/articles/trending`

### GET gossip articles
`vendor-server.herokuapp.com/regions/<region>/articles/gossip`

### GET tech articles
`vendor-server.herokuapp.com/regions/<region>/articles/tech`

### GET headlines articles
`vendor-server.herokuapp.com/regions/<region>/articles/headlines`

### GET business articles
`vendor-server.herokuapp.com/regions/<region>/articles/business`

## Pagination
The API responses are paginated. By default if no page number or size is specified, then the first page with a page size of 20 is returned.

Example:
`vendor-server.herokuapp.com/regions/<region>/articles/business?page=2&size=15`

This returns the second page in the result set of all Nigerian business articles in buckets of 15 each.

## Response
The API response looks like this:
```
{
  "count":772,
  "current_page":2,
  "first_page":1,
  "last_page":51,
  "previous_page":1,
  "next_page":3,
  "results":[
    {
      "id":"xxx",
      "title":"xxx",
      "source":"http://www.example.com/article/",
      "coverPic":"http://www.example.com/article/cover-pic.png",
      "section":"Business",
      "logo":"http://cdn.example.com/images/logo.png",
      "popularity":0,
      "mixIndex":3,
      "dateAdded":"2015-07-14T01:00:04.843000",
      "region":"nigeria"
    },
    {
      ...
    }
  ]
}
```
Where `results` holds the collection of articles being sought.
