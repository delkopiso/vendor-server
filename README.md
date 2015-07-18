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
