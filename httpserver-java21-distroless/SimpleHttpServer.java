import com.sun.net.httpserver.HttpContext;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;

public class SimpleHttpServer {
    private static final int listenPort = 8080;
    private static volatile long startupDuration = 0;

    public static void main(String[] args) throws IOException {
        long startTime = System.currentTimeMillis();

        HttpServer server = HttpServer.create(new InetSocketAddress(listenPort), 0);
        HttpContext context = server.createContext("/");
        context.setHandler(SimpleHttpServer::handleRequest);
        server.start();

        long endTime = System.currentTimeMillis();
        startupDuration = endTime - startTime;

        System.out.println("------------------------------------------------");
        System.out.println(" [Log] Server started in " + startupDuration + " ms!");
        System.out.println(" Waiting for connections...");
        System.out.println("------------------------------------------------");
    }

    private static void handleRequest(HttpExchange exchange) throws IOException {
        String response = "Hello, World!\n[Unikraft Speed] Boot time: " + startupDuration + " ms\n";
        exchange.sendResponseHeaders(200, response.getBytes().length);
        OutputStream os = exchange.getResponseBody();
        os.write(response.getBytes());
        os.close();
    }
}
