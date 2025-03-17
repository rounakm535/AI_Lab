from pyamaze import maze, COLOR, agent, textLabel


m = maze(15, 20)
m.CreateMaze(loopPercent=100)


a = agent(m, footprints=True, filled=True)
b = agent(m, 5, 5, footprints=True, color='red')
c = agent(m, 4, 1, footprints=True, color='green', shape='arrow')

path2 = [(5, 4), (5, 3), (4, 3), (3, 3), (3, 4), (4, 4)]
path3 = 'WWNNES'


l1 = textLabel(m, 'Total Cells', m.rows * m.cols)


m.tracePath({a: m.path, b: path2, c: path3}, delay=500, kill=True)


m.run()
