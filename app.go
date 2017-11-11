package main

import (
  "fmt"
  "net/http"
  _ "./routes/auth"
  // "./routes/postings"
  "./supports/types"
  "github.com/gorilla/mux"
)

/*
type Route struct{
  method  string
  path  string
  handler func(w http.ResponseWriter, r *http.Request)
}

var routes = make([]route, 0)

func RegisterRoute(r route){
  routes = append(routes, r)
}
*/
func main() {
  r := mux.NewRouter()
  fmt.Println(len(types.Routes))
  for _, rt := range(types.Routes){
    r.HandleFunc(rt.Path,rt.Handler).Methods(rt.Method)
  }
  http.ListenAndServe(":8080", nil)
}

func handle(w http.ResponseWriter, r *http.Request) {
  if r.URL.Path != "/" {
    http.NotFound(w, r)
    return
  }
  fmt.Fprint(w, "Hello world!")
}
