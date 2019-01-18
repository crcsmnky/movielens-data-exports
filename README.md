# MovieLens Data Exports

## MongoDB

Movies:
* `movieid`
* `year` and `title`: split from source data, which treated them as a single string
* `tmdb`: from links.csv
* `imdb`: from links.csv
* `poster`: using TMDB ID, retrieved a poster thumbnail URL
* `genres`: array of genre names
* `total_rating`: sum of all ratings values
* `ratings`: number of times the movie was rated
* `avg_rating`: computed from the previous two

Ratings:
* `userid`
* `movieid`
* `rating`
* `ts`

Genres:
* `name`
* `count`: count of all movies with this genre

Users:
* `userid`
* `ratings`

### Restore

Use `mongorestore` to restore the database.

```bash
mongorestore -d movielens mongodb/dump/
```

## Cloud Firestore

Movies:
* See [MongoDB Structure](#mongodb)

Genres:
* See [MongoDB Structure](#mongodb)

### Restore
First, copy the the `firestore` directory up to a Cloud Storage bucket:

```bash
gsutil -m cp -r firestore gs://YOUR-BUCKET/firestore
```

Then use the `firestore import` command to import the documents:

```bash
gcloud beta firestore import gs://YOUR-BUCKET/firestore
```

For more information, refer to [Export and import data](https://firebase.google.com/docs/firestore/manage-data/export-import) in the Firestore documentation.

## MySQL

Movies
* `movieid`
* `title`
* `year`
* `tmdb`
* `imdb`
* `poster`

Ratings:
* `userid`
* `movieid`
* `rating`
* `ts`

Genres:
* `genreid`
* `name`
* `count`

Genres_Movies:
* `genreid`
* `movieid`

### Restore

First, create the database in MySQL:

```bash
mysql> CREATE DATABASE movielens;
```
Then use the `mysql` client to restore the dataset to MySQL:

```bash
mysql -u user -p -d movielens < mysql/movielens.sql
```