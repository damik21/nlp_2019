import json
from nltk.tokenize import word_tokenize
from allennlp.commands.elmo import ElmoEmbedder

options_file = "./data/pubmed_elmo_model/elmo_2x4096_512_2048cnn_2xhighway_options.json"
weight_file = "./data/pubmed_elmo_model/elmo_2x4096_512_2048cnn_2xhighway_weights_PubMed_only.hdf5"

elmo = ElmoEmbedder(options_file, weight_file)

corpora_files = {
    "aimed": {
        "test": "./data/corpora/aimed/aimed_relations_test.txt",
        "train": "./data/corpora/aimed/aimed_relations_train.txt"
    },
    "cdr": {
        "test": "./data/corpora/cdr/test_relation_xu1.txt",
        "train": "./data/corpora/cdr/train_relation_xu1.txt"
    },
    "made": {
        "test": "./data/corpora/made/test_relation_xu.txt",
        "train": "./data/corpora/made/train_relation_xu.txt"
    }
}

# ресурсы, файлы которых используем в скрипте
# закомментить / раскомментить
resources = [
    "aimed",
    "cdr",
    "made"
]

for resource_name in resources:
    for file_type in ["test", "train"]:
        # все усреднённые векторы текущего файла
        averaged_vectors = []
        # открываем файл
        with open(corpora_files[resource_name][file_type]) as f:
            # пробегаемся по json-строкам
            for line in f:
                # преобразовываем json-строку в словарь
                relation_dict = json.loads(line)
                # количество слов в поле "middle_context" отношения
                middle_context_count = len(relation_dict['middle_context']) if relation_dict['middle_context'] else 0
                if middle_context_count == 0:
                    averaged_vectors.append([0] * 1024)
                    continue
                # заменяем в контексте $E1$ и $E2$ на текстовые значения данных сущностей
                context = relation_dict['context'] \
                    .replace("$E1$",
                             relation_dict['entity1']['text'] if relation_dict['entity1'] and relation_dict['entity1']
                             ['text'] else "") \
                    .replace("$E2$",
                             relation_dict['entity2']['text'] if relation_dict['entity2'] and relation_dict['entity2']
                             ['text'] else "")
                # токенизируем контекст
                tokenized_context = word_tokenize(context)
                # строим ELMO-вложения для токенизированного контекста
                context_embeddings = elmo.embed_sentence(tokenized_context)
                # P.S. context_embeddings содержит три 2d-вектора
                # "lower vectors represent more contextual information and higher vectors represent more semantics"
                # (информация из issue: https://github.com/allenai/allennlp/issues/1735)
                sentence = context_embeddings[0]
                # усреднённый вектор текущего отношения (итоговый размер равен длине вектора одного слова)
                averaged_vector = []
                # усредняем
                for i in range(1024):
                    elements_sum = 0
                    for vector in sentence:
                        elements_sum += vector[i]
                    averaged_value = elements_sum / middle_context_count
                    averaged_vector.append(averaged_value)
                averaged_vectors.append(averaged_vector)
