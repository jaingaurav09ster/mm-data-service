import subprocess
from random import randint


class Dockerise:


    def spin_docker_container(self, port):
        image_name = self.create_docker_image()
        port = str(port)+":"+str(port)
        subprocess.call(["docker", "run", "--add-host=localhost:192.168.99.1", "-d", "-p", port, image_name])

    def create_docker_image(self):
        image_name = "api"+str(randint(100, 999))
        subprocess.call(["docker", "build", "--tag", image_name, "../../"])
        return image_name


if __name__ == "__main__":
    import re
    print(re.sub("(?is)'DB_HOST':.+$", "'DB_HOST': 'host'", "'DB_HOST': 'localhost',", flags=re.M))
