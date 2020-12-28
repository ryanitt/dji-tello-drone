from easytello import tello

if __name__ == "__main__":
    drone = tello.Tello()

    while True:
        try:
            cmd = input("[Power " + str(drone.get_battery()) + "%]: ")
            print()

            if not cmd:
                print("invalid command")
                drone.land()
                break

            if 'quit' in cmd:
                print("Tello out...")
                drone.land()
                break
            else:
                drone.send_command(cmd)
        except (KeyboardInterrupt, AttributeError):
            print("invalid command sent")
            drone.land()
            break


