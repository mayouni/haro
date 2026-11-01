// The web comparison's Java server (webbench.py): the JDK's own com.sun.net.httpserver, a fixed pool of as many
// threads as the machine has cores. Run as a single source file (`java JavaServer.java <port>`), no build.
// The same three answers, byte for byte, as every server measured: /bench/hello, /bench/text, /bench/primes.
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.Collections;
import java.util.Locale;
import java.util.concurrent.Executors;

public class JavaServer {
    static final String P = String.join(" ", Collections.nCopies(20, "the quick brown fox jumps over the lazy dog"));

    static String text() {
        String[] words = P.split(" ");
        StringBuilder rev = new StringBuilder();
        for (int i = words.length - 1; i >= 0; i--) {
            rev.append(words[i]);
            if (i > 0) rev.append(' ');
        }
        return P.toUpperCase(Locale.ROOT) + "\n" + words.length + "\n" + rev;
    }

    // the primes below 20,000 by a sieve over an int array, Java's plain list of numbers
    static String primes() {
        int n = 20000, count = 0;
        int[] sieve = new int[n];
        for (int i = 2; i < n; i++) {
            if (sieve[i] == 0) {
                count++;
                for (long j = (long) i * i; j < n; j += i) sieve[(int) j] = 1;
            }
        }
        return Integer.toString(count);
    }

    static void answer(HttpExchange ex, String body) throws java.io.IOException {
        byte[] b = body.getBytes(StandardCharsets.UTF_8);
        ex.getResponseHeaders().set("Content-Type", "text/plain");
        ex.sendResponseHeaders(200, b.length);
        try (OutputStream o = ex.getResponseBody()) { o.write(b); }
    }

    public static void main(String[] args) throws Exception {
        int port = args.length > 0 ? Integer.parseInt(args[0]) : 8704;
        HttpServer s = HttpServer.create(new InetSocketAddress("127.0.0.1", port), 1024);
        s.createContext("/bench/hello", ex -> answer(ex, "hello"));
        s.createContext("/bench/text", ex -> answer(ex, text()));
        s.createContext("/bench/primes", ex -> answer(ex, primes()));
        s.setExecutor(Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors()));
        s.start();
    }
}
