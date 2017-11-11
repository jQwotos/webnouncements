package models

import (
  /* "net/http"
  "google.golang.org/appengine"
  "google.golang.org/appengine/log"
  "google.golang.org/appengine/datastore" */
)

type User struct {
  Email string
  PasswordHash  string
  Token string
}
