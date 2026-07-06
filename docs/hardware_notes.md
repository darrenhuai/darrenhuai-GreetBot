# Hardware Notes

GreetBot includes software that may be paired with robot hardware. Exact behavior depends on the physical components used in a build.

## Components to verify

- Camera model and mounting position
- Arduino board or compatible microcontroller
- Servo model and torque rating
- External power supply capacity
- USB or serial connection stability
- Physical range of motion for the handshake mechanism

## Integration checklist

- Confirm that the camera is detected by the operating system.
- Confirm that the microcontroller appears on the expected serial port.
- Test each servo with a small movement range before full motion.
- Keep wiring diagrams updated when hardware changes.
- Add a manual stop or disconnect procedure before live demos.

## Demo reliability

Before showing the robot publicly, run a short dry run that checks camera startup, serial communication, and mechanical movement separately. Debugging each subsystem independently makes failures easier to isolate.
