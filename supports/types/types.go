package types

import (
  "net/http"
)

type Route struct{
  Method  string
  Path  string
  Handler func(w http.ResponseWriter, r *http.Request)
}

var Routes = make([]Route, 0)

func RegisterRoute(r Route){
  Routes = append(Routes, r)
}
