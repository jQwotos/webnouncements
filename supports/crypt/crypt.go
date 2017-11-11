import (
  uuid "github.com/google/uuid"
  secrets "secrets"
  "crypto/sha256"
  "github.com/nu7hatch/gouuid"
)

func Encrypt(plainTextPass) {
  h := sha256.New()
  h.Write([]byte(plainTextPass + secrets.salt))
  return h.Sum(nil)
}

func Verify(plainTextPass, hashedPass) {
  if Encrypt(plainTextPass) == hashedPass {
    return true
  } else {
    return false
  }
}

func GenerateUUID() {
  u, _ := uuid.NewV4()
  return u
}
