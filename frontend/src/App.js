
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './stylesheets/App.css';
import FormView from './components/FormView';
import QuestionView from './components/QuestionView';
import Header from './components/Header';
import QuizView from './components/QuizView';

const App = () => {

  return (
    <div className='App'>
      <Header path />
      <Router>
        <Routes>
          <Route path='/' exact component={QuestionView} />
          <Route path='/add' component={FormView} />
          <Route path='/play' component={QuizView} />
          <Route path='*' component={QuestionView} />
        </Routes>
      </Router>
    </div>
  );

}


export default App;
