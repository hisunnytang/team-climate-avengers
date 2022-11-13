# Taken primarily from eco-faqs
import nltk
import pandas as pd
import os
import openai
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff
from typing import List
import numpy as np

from trafilatura import fetch_url, extract
from trafilatura.settings import use_config

trafilatura_cfg = use_config()
trafilatura_cfg.set("DEFAULT", "EXTRACTION_TIMEOUT", "0")


nltk.download("punkt")


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def get_embedding(
    text: str, engine="text-similarity-davinci-001"
) -> List[float]:
    """
    It takes a string of text and returns embeddings for the text

    :param text: The text to embed
    :type text: str
    :param engine: The name of the engine to use, defaults to text-similarity-davinci-001 (optional)
    :return: A list of floats.
    """
    # replace newlines, which can negatively affect performance.
    text = text.replace("\n", " ")

    return openai.Embedding.create(input=[text], engine=engine)["data"][0][
        "embedding"
    ]

def extract_text_from_url(url: str) -> str:
    """
    Extracts the text from the url, and returns the text
    :param url: the URL of the article to extract text from
    :type url: str
    :return: A string of text
    """
    print(f"Extracting text from {url}")
    downloaded = fetch_url(url)
    text_in = extract(downloaded, config=trafilatura_cfg)
    return text_in
  
 
def get_df_with_chunks_embedded(text: str) -> pd.DataFrame:
    """
    It splits the text into chunks, embeds each chunk, and returns a dataframe with the chunks and their embeddings

    :param text: The text to be split into chunks
    :type text: str
    :return: A dataframe with the chunks as rows and the search embedding as a column.
    """
    # Split the text into sentences (could also use TextWrap or something similar)
    sentences = nltk.sent_tokenize(text)

    # Determine the chunk size (empirically here 6 worked for this corpus)
    """ 
    You can also use GPT2 tokenizer in a smart way to chunk the test for example: 
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    def count_tokens(text: str) -> int:
      return len(tokenizer.encode(text))
    """
    chunk_size = len(sentences) // 6

    # Split the list of sentences into chunks
    chunks = [
      sentences[i : i + chunk_size]
      for i in range(0, len(sentences), chunk_size)
    ]

    # Concatenate the sentences in each chunk into a single string
    chunks = [" ".join(chunk) for chunk in chunks]

    # Create a dataframe with the chunks as rows
    df_with_chunks = pd.DataFrame(chunks, columns=["chunk"])

    df_with_chunks["search"] = df_with_chunks.chunk.apply(
      lambda x: get_embedding(x, engine="text-search-davinci-doc-001")
    )

    return df_with_chunks


def retrieve_text_embeddings(url_list: List[str],):
    """
    Create a database of embedding of credible source
    :param url_list: the list URL of the article to extract text from
    :return: pandas dataframe with the gpt3 embeddings
    :return: links that didn't work out
    """
    failed_links = []
    for link in url_list:
        
        text = extract_text_from_url(link)

        try:
          df = get_df_with_chunks_embedded(text)
        except:
          failed_links.append(link)

        total_request += len(df)

        df['source'] = link
        dfs.append(df)

        if total_request >= 30:
          sleep_now = True

        # we have limit on the requests per minute
        if sleep_now:

          # reset total_request
          total_request = 0
          print(f"total request = {total_request}")
          sleep_now = False
          time.sleep(60)
    return pd.concat(dfs), failed_links


def cosine_similarity(a, b):
    """
    It takes two vectors, a and b, and returns the cosine of the angle between them

    :param a: the first vector
    :param b: the number of bits to use for the hash
    :return: The cosine similarity between two vectors.
    """
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

  
def search_material(df: pd.DataFrame, query: str, n=3) -> pd.DataFrame:
    """
    It takes a query and a dataframe of search embeddings, and returns the top n most similar documents

    :param df: the dataframe containing the search column
    :type df: pd.DataFrame
    :param query: the query string
    :type query: str
    :param n: the number of results to return, defaults to 3 (optional)
    :return: A dataframe with the top n results from the search query.
    """
    embedding = get_embedding(query, engine="text-search-davinci-query-001")

    df["similarities"] = df.search.apply(
        lambda x: cosine_similarity(x, embedding)
    )

    res = df.sort_values("similarities", ascending=False).head(n)

    return res  
