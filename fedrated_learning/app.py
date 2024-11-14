import streamlit as st
import random

st.set_page_config(layout="wide")
st.title("Coding Practice Portal")

# Sample JSON structures for problems
easy_problems = [
    {
        "title": "Is Palindrome",
        "description": "Given a string `s`, return `true` if it is a palindrome, otherwise return `false`.",
        "explanation": "A palindrome is a string that reads the same forward and backward. It is also case-insensitive and ignores all non-alphanumeric characters.",
        "examples": [
            {
                "input": 's = "Was it a car or a cat I saw?"',
                "output": "true",
                "explanation": "After considering only alphanumeric characters, we have 'wasitacaroracatisaw', which is a palindrome."
            },
            {
                "input": 's = "tab a cat"',
                "output": "false"
            }
        ]
    },
    {
        "title": "Reverse Integer",
        "description": "Given a 32-bit signed integer `x`, return `x` with its digits reversed. If reversing `x` causes the value to go outside the signed 32-bit integer range, return 0.",
        "explanation": "Handle overflow by checking the reversed number’s range.",
        "examples": [
            {
                "input": 'x = 123',
                "output": "321"
            },
            {
                "input": 'x = -123',
                "output": "-321"
            },
            {
                "input": 'x = 1534236469',
                "output": "0",
                "explanation": "Reversing the number causes overflow, so the output is 0."
            }
        ]
    },
    {
        "title": "Valid Anagram",
        "description": "Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, otherwise return `false`.",
        "explanation": "An anagram is formed by rearranging the letters of a word to produce a new word, using all the original letters exactly once.",
        "examples": [
            {
                "input": 's = "anagram", t = "nagaram"',
                "output": "true"
            },
            {
                "input": 's = "rat", t = "car"',
                "output": "false"
            }
        ]
    },
    {
        "title": "Single Number",
        "description": "Given a non-empty array of integers `nums` where every element appears twice except for one, find that single one.",
        "explanation": "Use XOR for an efficient solution, as XOR of two identical numbers is 0.",
        "examples": [
            {
                "input": 'nums = [2, 2, 1]',
                "output": "1"
            },
            {
                "input": 'nums = [4, 1, 2, 1, 2]',
                "output": "4"
            }
        ]
    },
    {
        "title": "Fizz Buzz",
        "description": "Given an integer `n`, return a string array `answer` where `answer[i]` is 'FizzBuzz' if `i+1` is divisible by 3 and 5, 'Fizz' if `i+1` is divisible by 3, 'Buzz' if `i+1` is divisible by 5, or `i+1` otherwise.",
        "explanation": "Replace numbers divisible by 3 and 5 with 'FizzBuzz', only by 3 with 'Fizz', and only by 5 with 'Buzz'.",
        "examples": [
            {
                "input": 'n = 3',
                "output": '["1", "2", "Fizz"]'
            },
            {
                "input": 'n = 5',
                "output": '["1", "2", "Fizz", "4", "Buzz"]'
            },
            {
                "input": 'n = 15',
                "output": '["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"]'
            }
        ]
    }
]


medium_problems = [
    {
        "title": "3Sum",
        "description": "Given an integer array `nums`, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.",
        "explanation": "The solution set must not contain duplicate triplets.",
        "examples": [
            {
                "input": 'nums = [-1, 0, 1, 2, -1, -4]',
                "output": "[[-1, -1, 2], [-1, 0, 1]]"
            },
            {
                "input": 'nums = []',
                "output": "[]"
            }
        ]
    },
    {
        "title": "Longest Substring Without Repeating Characters",
        "description": "Given a string `s`, find the length of the longest substring without repeating characters.",
        "explanation": "Use a sliding window approach to track the longest substring without duplicates.",
        "examples": [
            {
                "input": 's = "abcabcbb"',
                "output": "3",
                "explanation": "The longest substring is 'abc', with length 3."
            },
            {
                "input": 's = "bbbbb"',
                "output": "1",
                "explanation": "The longest substring is 'b', with length 1."
            }
        ]
    },
    {
        "title": "Container With Most Water",
        "description": "Given an integer array `height` of length `n`, find two lines that together with the x-axis form a container, such that the container contains the most water.",
        "explanation": "Use a two-pointer approach to maximize the area between two lines in the array.",
        "examples": [
            {
                "input": 'height = [1,8,6,2,5,4,8,3,7]',
                "output": "49",
                "explanation": "The lines at index 1 and index 8 form the largest container."
            },
            {
                "input": 'height = [1,1]',
                "output": "1",
                "explanation": "The only container is formed by the two lines at indices 0 and 1."
            }
        ]
    },
    {
        "title": "Group Anagrams",
        "description": "Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.",
        "explanation": "Two words are anagrams if they have the same characters in the same frequencies. Sort or use a hashmap to group words by their character counts.",
        "examples": [
            {
                "input": 'strs = ["eat", "tea", "tan", "ate", "nat", "bat"]',
                "output": '[["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]'
            },
            {
                "input": 'strs = [""]',
                "output": '[[""]]'
            }
        ]
    },
    {
        "title": "Set Matrix Zeroes",
        "description": "Given an `m x n` integer matrix `matrix`, if an element is 0, set its entire row and column to 0. Do it in-place.",
        "explanation": "Use additional markers in the matrix to keep track of rows and columns to zero out, without using extra space for another matrix.",
        "examples": [
            {
                "input": 'matrix = [[1,1,1],[1,0,1],[1,1,1]]',
                "output": '[[1,0,1],[0,0,0],[1,0,1]]'
            },
            {
                "input": 'matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]',
                "output": '[[0,0,0,0],[0,4,5,0],[0,3,1,0]]'
            }
        ]
    }
]


hard_problems = [
    {
        "title": "Merge k Sorted Lists",
        "description": "You are given an array of `k` linked lists, each linked list is sorted in ascending order. Merge all the linked lists into one sorted linked list and return it.",
        "explanation": "Combine all the given sorted linked lists into a single sorted list.",
        "examples": [
            {
                "input": 'lists = [[1,4,5],[1,3,4],[2,6]]',
                "output": "[1,1,2,3,4,4,5,6]"
            }
        ]
    },
    {
        "title": "Trapping Rain Water",
        "description": "Given an array of non-negative integers `height` representing the elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
        "explanation": "Use two pointers to calculate the trapped water by comparing the height from left and right, while keeping track of the maximum height encountered from both sides.",
        "examples": [
            {
                "input": 'height = [0,1,0,2,1,0,1,3,2,1,2,1]',
                "output": "6",
                "explanation": "The water trapped is 6 units."
            },
            {
                "input": 'height = [4,2,0,3,2,5]',
                "output": "9",
                "explanation": "The water trapped is 9 units."
            }
        ]
    },
    {
        "title": "Wildcards Matching",
        "description": "Given an input string `s` and a pattern `p`, implement regular expression matching with support for `.` and `*` where:",
        "explanation": "The `.` character matches any single character, and `*` matches zero or more of the preceding element. Implement the matching algorithm using dynamic programming.",
        "examples": [
            {
                "input": 's = "aa", p = "a*"',
                "output": "true"
            },
            {
                "input": 's = "mississippi", p = "mis*is*p*."',
                "output": "false"
            }
        ]
    },
    {
        "title": "Edit Distance",
        "description": "Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2`. You have the following three operations permitted:",
        "explanation": "The allowed operations are insert a character, delete a character, or replace a character. Use dynamic programming to find the minimum number of operations.",
        "examples": [
            {
                "input": 'word1 = "horse", word2 = "ros"',
                "output": "3",
                "explanation": "Horse -> Ros: Replace 'h' with 'r', remove 'e', remove 's'."
            },
            {
                "input": 'word1 = "intention", word2 = "execution"',
                "output": "5"
            }
        ]
    },
    {
        "title": "Palindrome Partitioning II",
        "description": "Given a string `s`, partition `s` such that every substring of the partition is a palindrome. Return the minimum cuts needed for a palindrome partitioning of `s`.",
        "explanation": "Use dynamic programming to find the minimum cuts needed for palindrome partitioning by checking substrings for palindrome property.",
        "examples": [
            {
                "input": 's = "aab"',
                "output": "1",
                "explanation": "The optimal partitioning is ['aa', 'b'], requiring 1 cut."
            },
            {
                "input": 's = "a"',
                "output": "0",
                "explanation": "The string 'a' is already a palindrome, so no cuts are needed."
            }
        ]
    }
]


# Sidebar navigation for difficulty levels
st.sidebar.title("Difficulty Levels")
difficulty = st.sidebar.radio("Select difficulty", ["Easy", "Medium", "Hard"])

# Function to display questions based on difficulty
def display_question(difficulty):
    if difficulty == "Easy":
        problems = easy_problems
    elif difficulty == "Medium":
        problems = medium_problems
    elif difficulty == "Hard":
        problems = hard_problems
    else:
        problems = []

    if problems:
        question = random.choice(problems)  # Randomly pick a question from the list
        st.subheader(question["title"])
        st.markdown(f"<h5 style='color:green;'>{difficulty}</h5>", unsafe_allow_html=True)
        st.write(question["description"])
        st.write(question["explanation"])
        
        for i, example in enumerate(question["examples"], start=1):
            st.markdown(f"### Example {i}:")
            st.code(f"Input: {example['input']}\nOutput: {example['output']}", language="text")
            if "explanation" in example:
                st.write(f"Explanation: {example['explanation']}")

# Display the question based on selected difficulty
display_question(difficulty)

# Main column for code editor and language selection
with st.container():
    st.write("### Select Language")
    language = st.selectbox("", ["Python", "Java", "C++", "JavaScript", "C#"], key="language_select", label_visibility="collapsed")
    
    st.write("### Write your solution here:")
    code_input = st.text_area("", height=300, value="def solution():\n    # Write your code here\n    pass", key="code_input", label_visibility="collapsed")
    
    # Buttons for running and submitting code
    col_run, col_submit = st.columns([1, 1])
    with col_run:
        if st.button("Run"):
            st.write("Code is running... (simulated)")  # Placeholder for code execution
    with col_submit:
        if st.button("Submit"):
            st.write("Code submitted!")  # Placeholder for submission logic
