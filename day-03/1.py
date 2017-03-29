class Queue:
    list = []

    def push(self, el):
        new_list = [el]
        new_list.extend(self.list)
        self.list = new_list

    def pull(self):
        try:
            print(self.list.pop())
        except Exception as e:
            print(e)

    def get(self):
        return self.list


queue = Queue()

queue.push(1)
queue.push(2)
queue.push(3)
queue.push(4)
queue.push(5)
queue.push(6)

queue.pull()
queue.pull()
queue.pull()
queue.pull()
queue.pull()
queue.pull()
queue.pull()

print(queue.get())
