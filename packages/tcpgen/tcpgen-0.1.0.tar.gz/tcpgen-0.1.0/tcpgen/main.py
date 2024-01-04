import sys
import socket


def prompt_host():
    hostname_or_ip = input("Hostname/IP: ")
    host = resolve_host(hostname_or_ip)
    return host


def prompt_ports():
    ports = ""
    while not ports:
        ports = input("Ports (separated by space, e.g. 22 80 443): ")
    if ports[0] == " ":
        ports = ports[1:]
    if ports[-1] == " ":
        ports = ports[:len(ports) - 1]
    ports = ports.split(" ")
    for i, port in enumerate(ports):
        ports[i] = int(port)
    
    return ports


def resolve_host(hostname_or_ip):
    if hostname_or_ip[-1] == " ":
        target = hostname_or_ip[:len(hostname_or_ip) - 1]
    else:
        target = hostname_or_ip
    host = socket.gethostbyname(target)
    if host != target:
        print(f"Resolved {target} to {host}")
    return host


def main():
    DEFAULT_PORTS = [22]
    socket.setdefaulttimeout(2)
    infinite_loop = len(sys.argv) <= 1

    while True: 
        host = ""
        ports = []

        try:
            if len(sys.argv) == 1:
                host = prompt_host()
                ports = prompt_ports()

            elif len(sys.argv) == 2:
                hostname_or_ip = sys.argv[1]
                host = resolve_host(hostname_or_ip)
                ports = DEFAULT_PORTS

            else:
                hostname_or_ip = sys.argv[1]
                host = resolve_host(hostname_or_ip)
                for port in sys.argv[2:]:
                    ports.append(int(port))

        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit()
        except socket.gaierror:
            print("Hostname could not be resolved.")
            if not infinite_loop:
                sys.exit()
        except ValueError:
            print("Invalid port.")
            if not infinite_loop:
                sys.exit()
        except Exception as e:
            print("Error encountered:")
            print(e)
            sys.exit()

        for port in ports:
            exit_early = False
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                s.connect((host, port))
                print(f"{port}: SUCCESS")

            except KeyboardInterrupt:
                print("\nExiting...")
                exit_early = True
            except socket.error as e:
                print(f"{port}:", e)
            except Exception as e:
                print("Error encountered:")
                print(e)
                exit_early = True
            finally:
                s.close()
                if exit_early:
                    exit()

        if not infinite_loop:
            break
        else:
            print()
        
if __name__ == "__main__":
    main()
