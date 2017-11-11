package auth

import (
  "fmt"
  // "log"
  "net/http"
  "encoding/json"
  // "../../app"
  // "google.golang.org/appengine"
  // "golang.org/x/net/context"
  "../../supports/models"
  // "../../secrets"
  // "../../app"
  "../../supports/types"
)

func init(){
  types.RegisterRoute(types.Route{
      Method:"POST",
      Path:"/auth/create",
      Handler:create})
  /*
  registerRoute(types.route{
    method="POST",
    path="/auth/signin",
    handler=login
  })
  */
}

func create(w http.ResponseWriter, r *http.Request){
  var u models.User
  err := json.NewDecoder(r.Body).Decode(&u)

  if err != nil {
    http.Error(w, err.Error(), 400)
    return
  }
  /*
  c := appengine.NewContext(u)
  g := User{
    email: u.email,
    passwordHash:
  }
  */
  fmt.Println(u.Email)
  return
}
