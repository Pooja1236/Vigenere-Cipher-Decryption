import streamlit as st
import json
from streamlit_lottie import st_lottie
import string
from collections import Counter

st.set_page_config(page_title="Unlock the Vigenère Cipher: Decryption & Key Finder", page_icon= ":tada:", layout="wide")

with st.container():
    st.title("Easily decrypt Vigenère Cipher messages and uncover encryption keys")
    st.subheader("Handles large encrypted messages with ease and accuracy.")
    st.write("Decrypt the Vigenère Cipher! Because even scientists need a little mystery in their lives.")
    st.write("[Learn More >](https://www.geeksforgeeks.org/vigenere-cipher/)")

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_coding = load_lottiefile(r"Animation - 1716145550728.json")

def vigenere_decrypt(ciphertext, key):
    decrypted_text = ""
    key_length = len(key)
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            if char.isupper():
                shift = ord(key[key_index % key_length].upper()) - ord('A')
                decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                shift = ord(key[key_index % key_length].upper()) - ord('A')
                decrypted_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            decrypted_text += decrypted_char
            key_index += 1
        else:
            decrypted_text += char

    return decrypted_text

def find_vigenere_key(ciphertext, max_key_length=15):
    # Remove non-alphabetic characters and convert to uppercase
    ciphertext = ''.join(filter(str.isalpha, ciphertext)).upper()
    text_length = len(ciphertext)

    # Step 1: Determine key length using Index of Coincidence (IC) or Kasiski examination
    candidate_key_lengths = []
    for length in range(2, max_key_length + 1):
        # Calculate Index of Coincidence (IC) for the given key length
        sum_ic = 0.0
        for i in range(length):
            # Gather characters at positions i, i+length, i+2*length, ...
            subset = [ciphertext[j] for j in range(i, text_length, length)]
            subset_counts = Counter(subset)
            subset_length = len(subset)
            # Calculate IC for this subset
            if subset_length > 1:
                sum_ic += sum(count * (count - 1) for count in subset_counts.values()) / (subset_length * (subset_length - 1))

        # Average IC for this key length
        average_ic = sum_ic / length
        # Compare with expected IC values for different key lengths
        # Adjust the threshold based on language and text characteristics
        if average_ic > 0.055:  # Adjust threshold as needed
            candidate_key_lengths.append(length)

    # Step 2: Guess the key using the determined key length(s)
    possible_keys = []
    for length in candidate_key_lengths:
        # Attempt to deduce key by frequency analysis on shifted characters
        key = []
        for i in range(length):
            # Gather characters at positions i, i+length, i+2*length, ...
            subset = [ciphertext[j] for j in range(i, text_length, length)]
            subset_counts = Counter(subset)
            # Determine the most frequent letter in the subset
            # Estimate the key letter based on letter frequencies
            most_common_letter = subset_counts.most_common(1)[0][0]
            estimated_key_letter = chr((ord(most_common_letter) - ord('E')) % 26 + ord('A'))
            key.append(estimated_key_letter)

        possible_keys.append(''.join(key))

    return possible_keys

with st.container():
    left_column, right_column = st.columns(2)

    with left_column:
        st.write("### Enter Encrypted Message")
        ciphertext = st.text_area("Encrypted message", height=200)

        st.write("### Enter Key (Optional)")
        key = st.text_input("Key (if known)", "")
        
        if st.button("Decrypt"):
            if key:
                decrypted_message = vigenere_decrypt(ciphertext, key)
                st.write(f"### Decrypted Message with Key '{key}'")
                st.write(decrypted_message)
            else:
                possible_keys = find_vigenere_key(ciphertext)
                if possible_keys:
                    st.write("### Possible Keys and Decrypted Messages")
                    for key in possible_keys:
                        decrypted_message = vigenere_decrypt(ciphertext, key)
                        st.write(f"**Key: {key}**")
                        st.write(decrypted_message)
                else:
                    st.write("No possible keys found.")

    with right_column:
        st_lottie(
            lottie_coding,
            speed=1,
            reverse=False,
            loop=True,
            quality="high",
            height=None,
            width=None,
            key=None
        )
