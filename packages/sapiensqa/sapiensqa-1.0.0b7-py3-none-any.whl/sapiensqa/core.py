class SapiensQA:
    def __init__(self, temperature=.01): self.__dataset, self.__temperature = [], 1-min((max((0, float(temperature)))), 1) if type(temperature) in (int, float) else .99
    def __normalization(self, text=''):
        text = str(text).strip()
        from unicodedata import category
        normalization = lambda text: ''.join(c for c in __import__('unicodedata').normalize('NFD', text) if category(c) != 'Mn' and (c.isalnum() or c.isspace()))
        text = normalization(text).lower()
        return text
    def __is_number(self, token=''):
        try: return type(float(str(token).strip())) == float
        except: return False
    def __mask(self, string=''): return chr(32).join([token[:-3] if len(token) > 5 and not self.__is_number(token) else token for token in string.split()])
    def __tokenizer(self, text=''): return str(text).strip().split(chr(32))
    def __embedding(self, tokens=[], _type='encoding'): return [[ord(char) for char in token] for token in tokens] if _type == 'encoding' else [[chr(number) for number in token] for token in tokens]
    def __semantic_comparison(self, input=''):
        input = str(input).strip()
        input = self.__mask(self.__normalization(input))
        input_tokens = self.__embedding(tokens=self.__tokenizer(input), _type='encoding')
        positional_encodings, positional_encoding, maximum_coincidence = [], 0, 0
        for index, tokens_x in enumerate(self.__dataset):
            tokens_x, coincidences = tokens_x['input'], 0
            if input_tokens == tokens_x:
                positional_encoding = index
                break
            else:
                matrix_a, matrix_b = input_tokens, tokens_x
                vectorization = [[abs(a-b)/max((a, b)) for a, b in zip(vector_a, vector_b)] for vector_a, vector_b in zip(matrix_a, matrix_b)]
                probabilities = [sum(odds)/len(odds) for odds in vectorization]
                probability = 1-(sum(probabilities)/len(probabilities))
                if probability >= self.__temperature: positional_encodings.append(index)
                else:
                    for token_y in input_tokens:
                        if token_y in tokens_x: coincidences += 1
                    if coincidences >= maximum_coincidence: maximum_coincidence, positional_encoding = coincidences, index
        if positional_encoding not in positional_encodings: positional_encodings.append(positional_encoding)
        from random import choice
        election = choice(positional_encodings) if len(positional_encodings) > 0 else 0
        return self.__dataset[election]['output'] if len(self.__dataset) > 0 else ''
    def __insert_fine_tuning(self, question='', answer=''):
        question, answer = str(question).strip(), str(answer).strip()
        if len(question.split(chr(32))) > 1 and len(answer) > 0 and len(answer.split(chr(32))) > 0:
            if (answer[0] == chr(34) and answer.count(chr(34)) == 1) or (answer[0] == chr(39) and answer.count(chr(39)) == 1): answer = answer[1:]
            elif (answer[-1] == chr(34) and answer.count(chr(34)) == 1) or (answer[-1] == chr(39) and answer.count(chr(39)) == 1): answer = answer[:-1]
            elif answer.count(chr(34)) == 1: answer = answer.replace(chr(34), '')
            self.fineTuning(question=question, answer=answer)
    def fit(self, path='', show_progress=True):
        try:
            path, show_progress, text, delimiter = str(path).strip(), bool(show_progress) if type(show_progress) in (int, float, bool) else True, '', chr(9)
            extension = path.rpartition(chr(46))[-1].lower().strip() if chr(46) in path else ''
            from re import compile
            pattern = compile(r'^(http://|https://)')
            from os import path as _path
            if len(path) <= 0 or (not _path.exists(path) and not pattern.match(path)): return
            if extension == 'txt':
                with open(path, 'r', encoding='utf-8') as file: text = str(file.read()).strip()
            elif extension == 'pdf':
                if pattern.match(path):
                    from urllib.request import Request, urlopen
                    from io import BytesIO
                    from PyPDF2 import PdfReader
                    request = Request(path, headers={'User-Agent': 'Magic Browser'})
                    remote_file = urlopen(request).read()
                    remote_file_bytes = BytesIO(remote_file)
                    remote_pdf_document = PdfReader(remote_file_bytes)
                    for index in range(len(remote_pdf_document.pages)):
                        current_page = remote_pdf_document.pages[index]
                        text += str(current_page.extract_text()).strip()+'\n'
                else:
                    from pdfplumber import open as open_pdf
                    with open_pdf(path) as file:
                        for page_text in file.pages: text += str(page_text.extract_text()).strip()+'\n'
            elif extension == 'docx':
                from docx2txt import process
                text = str(process(path)).strip()
            elif pattern.match(path):
                from requests import get
                from bs4 import BeautifulSoup
                response = get(path)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    paragraphs = soup.find_all('p')
                    for paragraph in paragraphs:
                        paragraph = str(paragraph.get_text()).strip()
                        if len(paragraph.split(chr(32))) > 2: text += paragraph+'\n'
            if len(text.strip()) > 0:
                from re import sub
                text = sub(r'\n{2,}', chr(10), sub(r'\s{2,}', chr(32), text.strip()))
                text = text.replace(chr(8220), chr(34)).replace(chr(8221), chr(34))
                text = text.replace(chr(171),  chr(34)).replace(chr(187),  chr(34))
                text = text.replace(chr(8216), chr(39)).replace(chr(8219), chr(39))
                text = text.replace(chr(8222), chr(34)).replace(chr(8223), chr(34))
                text = text.replace(chr(8249), chr(39)).replace(chr(8250), chr(39))
                delimiters = (chr(46)+chr(10), chr(46)+chr(32), chr(10), chr(59), chr(33), chr(44), chr(42), chr(95))
                for element in delimiters:
                    if text.count(element) > 1:
                        delimiter = element
                        break
                sentences = text.split(delimiter)
                if len(sentences) > 0:
                    total_sentences = len(sentences)
                    for epoch, sentence in enumerate(sentences):
                        if len(sentence.strip()) > 0:
                            asking = False
                            if sentence.count(chr(63)) == 1:
                                question, answer = sentence.split(chr(63))
                                asking = True
                            elif sentence.count(chr(58)) == 1:
                                question, answer = sentence.split(chr(58))
                                asking = True
                            else:
                                attention = chr(32).join([token for token in sentence.split(chr(32)) if len(token) > 3 or token.isupper() or self.__is_number(token)])
                                question, answer = attention, sentence+delimiter
                            if asking and delimiters[1] in question:
                                parts = question.split(delimiters[1])
                                question = parts[-1]
                                for part in parts[:-1]: self.__insert_fine_tuning(question=part, answer=part+delimiters[1])
                            self.__insert_fine_tuning(question=question, answer=answer)
                        if show_progress:
                            percentage = ((epoch+1)/total_sentences)*100
                            str_percentage = f'{percentage:.10f}%'
                            str_percentage = str_percentage.rjust(15, '0')
                            print(f'Training progress: {str_percentage}')
        except Exception as error: print('ERROR during training: '+str(error))
    def fineTuning(self, question='', answer=''):
        try:
            question, answer = str(question).strip(), str(answer).strip()
            if len(question) > 0 and len(answer) > 0:
                question = self.__mask(self.__normalization(question))
                input_tokens = self.__embedding(tokens=self.__tokenizer(question), _type='encoding')
                output_tokens = self.__embedding(tokens=self.__tokenizer(answer), _type='encoding')
                input_output = {"input": input_tokens, "output": output_tokens}
                self.__dataset.append(input_output)
        except Exception as error: print('ERROR during fine tuning: '+str(error))
    def saveModel(self, path=''):
        try:
            path = str(path).strip()
            if len(path) <= 3: path = 'SapiensQA-Model.qa'
            if path[-3:].lower() != '.qa': path += '.qa'
            from json import dumps
            model = dumps(self.__dataset)
            from re import sub
            parameters = sub(r'[^0-9\s]', '', str(model).strip())
            parameters_count = len(parameters.split(chr(32)))
            if parameters_count < 1000: model_size = f'{parameters_count}P'
            elif parameters_count < 1_000_000: model_size = f'{parameters_count // 1000}K'
            elif parameters_count < 1_000_000_000: model_size = f'{parameters_count // 1_000_000}M'
            elif parameters_count < 1_000_000_000_000: model_size = f'{parameters_count // 1_000_000_000}B'
            else: model_size = f'{parameters_count // 1_000_000_000_000}T'
            binary_data = ''.join(format(ord(char), '08b') for char in model)
            if path[-3:].lower() == '.qa': path = path[:-3]+f'-{model_size}.qa'
            with open(path, 'w', encoding='utf-8') as file: file.write(binary_data)
        except Exception as error: print('ERROR during saving model: '+str(error))
    def loadModel(self, path=''):
        try:
            path = str(path).strip()
            if len(path) <= 3: path = 'SapiensQA-Model.qa'
            if path[-3:].lower() != '.qa': path += '.qa'
            from os import path as _path
            if not _path.exists(path): return
            with open(path, 'r', encoding='utf-8') as file: binary_data = str(file.read()).strip()
            original_string = ''.join(chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8))
            from json import loads
            try: self.__dataset = loads(original_string)
            except:
                from ast import literal_eval
                self.__dataset = literal_eval(original_string)
        except Exception as error: print('ERROR during loading model: '+str(error))
    def transferLearning(self, transmitter_path='', receiver_path='', rescue_path=''):
        try:
            transmitter_path, receiver_path, rescue_path = str(transmitter_path).strip(), str(receiver_path).strip(), str(rescue_path).strip()
            from os import path
            if len(transmitter_path) <= 0 or len(receiver_path) <= 0 or not path.exists(transmitter_path) or not path.exists(receiver_path): return
            self.loadModel(path=transmitter_path)
            from copy import deepcopy
            transmitter_dataset = deepcopy(self.__dataset)
            self.loadModel(path=receiver_path)
            self.__dataset += transmitter_dataset
            self.saveModel(path=rescue_path)
        except Exception as error: print('ERROR during transferring learning: '+str(error))
    def predict(self, question=''):
        try:
            question = str(question).strip()
            if len(question) <= 0: return ''
            output_tokens = self.__semantic_comparison(input=question)
            answer = chr(32).join([''.join(embeddings) for embeddings in self.__embedding(tokens=output_tokens, _type='decoding')])
            return answer
        except Exception as error:
            print('ERROR during prediction: '+str(error))
            return ''
    def printPrediction(self, question='', wait=1):
        try:
            answer = self.predict(question=question)
            tokens = answer.split(chr(32))
            number_of_tokens = max((1, len(tokens)))
            wait = max((0, float(wait))) if type(wait) in (int, float) else 1
            from time import sleep
            for index, token in enumerate(tokens):
                sleep(wait/number_of_tokens)
                completion = chr(32) if index < (number_of_tokens-1) else chr(10)
                print(token, end=completion, flush=True)
        except Exception as error: print('ERROR during prediction printing: '+str(error))
