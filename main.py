import extract_data
import topsis

# Do testowania działania rankingu
def ranking(data_, result_):
    print("Ranking")
    for i in range(len(result_)):
        print(f"{i+1}. {data_[1][result_[i]][1]}, {data_[1][result_[i]][2]}")

if __name__ == "__main__":
    r = extract_data.get_data_from_database()

    print(r[3])

    lower_limits_ = [0 for i in range(12)]
    upper_limits_ = [15000 for i in range(12)]
    weight_vector_ = [1 / 12 for i in range(12)]
    benefit_attributes_ = [1 for i in range(12)]

    result_ = topsis.topsis(r[3], lower_limits_, upper_limits_, weight_vector_, benefit_attributes_)
    ranking(r, result_)