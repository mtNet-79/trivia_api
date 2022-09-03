import React, { Component, useEffect, useState } from 'react';
import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';



const QuestionView = () => {
  const [values, setValues] = useState({
    questions: [],
      page: 1,
      totalQuestions: 0,
      categories: {},
      currentCategory: null,
  })

  useEffect(() => {
    getQuestions()
  })

  const getQuestions = () => {
    $.ajax({
      url: `/questions?page=${page}`, //TODO: update request URL
      type: 'GET',
      success: (result) => {
        setValues({
          questions: result.questions,
          totalQuestions: result.total_questions,
          categories: result.categories,
          currentCategory: result.current_category,
        });
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  function selectPage(num) {
    setValues({...values, page:num});
    console.log("values: ", values);
  }

  function createPagination() {
    let pageNumbers = [];
    let maxPage = Math.ceil(values.totalQuestions / 10);
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === values.page ? 'active' : ''}`}
          onClick={selectPage(i)}
        >
          {i}
        </span>
      );
    }
    return pageNumbers;
  }

  const getByCategory = (id) => {
    $.ajax({
      url: `/categories/${id}/questions`, //TODO: update request URL
      type: 'GET',
      success: (result) => {
        setValues({
          ...values,
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category,
        });
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  const submitSearch = (searchTerm) => {
    $.ajax({
      url: `/questions`, //TODO: update request URL
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({ searchTerm: searchTerm }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        setValues({
          ...values,
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category,
        });
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  const questionAction = (id) => (action) => {
    if (action === 'DELETE') {
      if (window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: `/questions/${id}`, //TODO: update request URL
          type: 'DELETE',
          success: (result) => {
            getQuestions();
          },
          error: (error) => {
            alert('Unable to load questions. Please try your request again');
            return;
          },
        });
      }
    }
  };

 
    return (
      <div className='question-view'>
        <div className='categories-list'>
          <h2
            onClick={() => {
              getQuestions();
            }}
          >
            Categories
          </h2>
          <ul>
            {Object.keys(values.categories).map((id) => (
              <li
                key={id}
                onClick={() => {
                  getByCategory(id);
                }}
              >
                {values.categories[id]}
                <img
                  className='category'
                  alt={`${values.categories[id].toLowerCase()}`}
                  src={`${values.categories[id].toLowerCase()}.svg`}
                />
              </li>
            ))}
          </ul>
          <Search submitSearch={submitSearch} />
        </div>
        <div className='questions-list'>
          <h2>Questions</h2>
          {values.questions.map((q, ind) => (
            <Question
              key={q.id}
              question={q.question}
              answer={q.answer}
              category={values.categories[q.category]}
              difficulty={q.difficulty}
              questionAction={questionAction(q.id)}
            />
          ))}
          <div className='pagination-menu'>{createPagination()}</div>
        </div>
      </div>
    );
  
}

export default QuestionView;
