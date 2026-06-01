// launcher wraps `spin up`, waits for the HTTP listener to bind, then — if
// TEMPLATE=1 — writes to /uk/libukp/template_instance so Unikraft Cloud can
// snapshot the running instance for template-based deployment.
package main

import (
	"log"
	"net"
	"os"
	"os/exec"
	"os/signal"
	"syscall"
	"time"
)

const (
	spinBin      = "/usr/bin/spin"
	readyAddr    = "127.0.0.1:3000"
	templateFile = "/uk/libukp/template_instance"
)

func main() {
	cmd := exec.Command(spinBin, os.Args[1:]...)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	if err := cmd.Start(); err != nil {
		log.Fatalf("spin start failed: %v", err)
	}

	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGTERM, syscall.SIGINT)
	go func() {
		for s := range sigs {
			_ = cmd.Process.Signal(s)
		}
	}()

	go func() {
		for {
			c, err := net.DialTimeout("tcp", readyAddr, 100*time.Millisecond)
			if err == nil {
				_ = c.Close()
				break
			}
			time.Sleep(50 * time.Millisecond)
		}
		if os.Getenv("TEMPLATE") != "1" {
			return
		}
		if err := os.WriteFile(templateFile, []byte("1"), 0644); err != nil {
			log.Printf("template signal failed: %v", err)
		}
	}()

	if err := cmd.Wait(); err != nil {
		if exitErr, ok := err.(*exec.ExitError); ok {
			os.Exit(exitErr.ExitCode())
		}
		log.Fatalf("spin wait failed: %v", err)
	}
}
