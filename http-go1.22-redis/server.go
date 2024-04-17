package main

import (
	"context"
	"fmt"
	"net/http"
	"os"

	"github.com/redis/go-redis/v9"
)

var (
	ctx = context.Background()
	rdb *redis.Client
)

func get(w http.ResponseWriter, req *http.Request) {
	key := req.FormValue("key")

	val, err := rdb.Get(ctx, key).Result()
	if err != nil {
		fmt.Fprintf(w, "Error accessing key: %s\n", err.Error())
		return
	}

	fmt.Printf("Getting key \"%s\" has value \"%s\"\n", key, val)

	fmt.Fprintf(w, "Key \"%s\" has value \"%s\"\n", key, val)
}

func put(w http.ResponseWriter, req *http.Request) {
	key := req.FormValue("key")
	if key == "" {
		fmt.Fprintf(w, "Key is required!\n")
		return
	}

	val := req.FormValue("value")
	if val == "" {
		fmt.Fprintf(w, "Value is required!\n")
		return
	}

	err := rdb.Set(ctx, key, val, 0).Err()
	if err != nil {
		fmt.Fprintf(w, "Error accessing key: %s\n", err.Error())
	}

	fmt.Printf("Setting key \"%s\" to value \"%s\"\n", key, val)

	fmt.Fprintf(w, "Success!\n")
}

func main() {
	addr := os.Getenv("REDIS_ADDR")
	if addr == "" {
		addr = "redis:6379"
	}

	rdb = redis.NewClient(&redis.Options{
		Addr:     addr,
		Password: os.Getenv("REDIS_PASS"),
		DB:       0,
	})

	http.HandleFunc("GET /", get)
	http.HandleFunc("POST /", put)

	fmt.Println("Listening on :8080...")

	http.ListenAndServe(":8080", nil)
}
