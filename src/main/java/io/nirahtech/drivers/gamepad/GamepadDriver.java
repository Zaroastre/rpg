package io.nirahtech.drivers.gamepad;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.util.Objects;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import io.nirahtech.drivers.Driver;
import io.nirahtech.drivers.Event;
import io.nirahtech.drivers.InputDevice;

public class GamepadDriver implements Driver {
    private static final int PORT = 44_666;
    private InputDevice device;
    private final ExecutorService executorService;
    private Event previousEvent = null;

    public GamepadDriver() {
        this.executorService = Executors.newSingleThreadExecutor();
        this.executorService.submit(() -> {
            final ProcessBuilder processBuilder = new ProcessBuilder();
            processBuilder.command("python", "src/main/resources/drivers/gamepad.py", "--port", String.valueOf(PORT));
            Process process;
            try {
                process = processBuilder.start();
                final int exitCode = process.waitFor();
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            } catch (InterruptedException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }

        });
    }

    @Override
    public void setController(InputDevice device) {
        this.device = device;
    }

    @Override
    public void start() {
        final Thread runtime = new Thread(() -> {
            try (final DatagramSocket server = new DatagramSocket(PORT)) {
                final byte[] data = new byte[1024];
                while (!this.executorService.isShutdown()) {
                    final DatagramPacket packet = new DatagramPacket(data, data.length);
                    server.receive(packet);
                    final String payload = new String(packet.getData(), 0, packet.getLength());
                    final GamepadEvent event = GamepadEvent.parse(payload);
                    if (Objects.nonNull(this.device) && Objects.nonNull(event)) {
                        this.handle(event);
                    }
    
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        });
        runtime.start();
    }

    @Override
    public void stop() {
        this.executorService.shutdownNow();
    }

    @Override
    public void handle(Event event) {
        if (Objects.isNull(this.previousEvent)) {
            this.previousEvent = event;
        }

        if (Objects.nonNull(this.previousEvent)) {
            if (!event.equals(this.previousEvent)) {
                this.previousEvent = event;
                this.device.handle(event);
            }
        }
    }
    
}
