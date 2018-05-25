import csv

from shard.utils.consistent_hash.pool import ConHashPool

filename = 'data.csv'
nodes = [f'library_{index}' for index in range(16)]
pool = ConHashPool(
    nodes=nodes,
    replica=128
)


def associate_data():
    result = dict((node, {
        'total': 0,
        'count_per_user': {}
    }) for node in nodes)
    with open(filename) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            u_idx = row['u_idx']
            b_id = row['b_id']

            node_index = pool.get_node(value=u_idx).index
            node = nodes[node_index]

            if u_idx not in result[node]['count_per_user']:
                result[node]['count_per_user'][u_idx] = {}

            if b_id not in result[node]['count_per_user'][u_idx]:
                result[node]['count_per_user'][u_idx][b_id] = 0

            result[node]['total'] += 1
            result[node]['count_per_user'][u_idx][b_id] += 1

    return result


def print_result():
    data = associate_data()

    with open('result.csv', 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')

        for node in nodes:
            writer.writerow([node, len(data[node]['count_per_user'].keys()), data[node]['total']])


if __name__ == '__main__':
    print_result()
