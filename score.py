def cal_score(score_points, coin_count, time_taken, enemy_kills = 0):
    score_points += (coin_count + enemy_kills * 2) * 50
    score_points -= (time_taken) * 100
    return score_points



def score_keeping(path,score_points, info, name = ''): #info = [coin, time, enemy_kills]
    coin_count = info[0]
    time_taken = info[1]
    enemy_kills = info[2]
    repeat_name = False
    no_name = False

    score_points = int(cal_score(score_points, coin_count, time_taken, enemy_kills))

    f = open(path + 'score', 'r')
    data = f.read()
    f.close()
    current_name_score = {}
    for line in data.split('\n'):
        if line == '':
            no_name = True
            break
        sections = line.split(' ')
        player_name = sections[0]
        if name != '':
            current_name_score[player_name] = sections[1]
    sorted_score = {player_name: score for player_name, score in sorted(current_name_score.items(), key = lambda score: score[1], reverse = True)}
    for players in sorted_score.keys():
        if name == players:
            sorted_score[name] = max(int(sorted_score[players]), int(score_points))
            repeat_name = True
        else:
            pass
    if not(repeat_name):
        sorted_score[name] = score_points
    f = open(path + 'score', 'w')
    n = 0
    for key in sorted_score.keys():
        if no_name:
            if name == '':
                f.write(str(sorted_score[key]))
            else:
                f.write(key + ' ' + str(sorted_score[key]))
            no_name = False
        elif n == 0:
            if name == '':
                f.write(str(sorted_score[key]))
            else:
                f.write(key + ' ' + str(sorted_score[key]))
        else:
            if name == '':
                f.write('\n' + str(sorted_score[key]))
            else:
                f.write('\n' + key + ' ' + str(sorted_score[key]))
        n += 1
    f.close()
    return score_points


