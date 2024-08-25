describe('Test cases for R8UC1', () => {
  // Variables to store user information
  let uid;
  let email;
  let task_id;
  let todo_id;
  // Before hook to create a user and login before each test
  before(function() {
    cy.fixture('user.json').then((user) => {
      // Create a user
      cy.request({
        method: 'POST',
        url: 'http://localhost:5000/users/create',
        form: true,
        body: user
      }).then((response) => {
        uid = response.body._id.$oid;
        email = user.email;
      });
    });
    cy.fixture("NewTask.json")
    .then(task => {
      cy.request({
        method: "POST",
        url: "http://localhost:5000/tasks/create",
        form: true,
        body: {
          ...task,
          "userid": uid
        }
      }).then(response => {
        task_id = response.body[0]._id.$oid
        todo_id = response.body[0].todos[0]._id.$oid;
      })
    })
  });
  // Before each hook to login before each test
  beforeEach(function(){
    cy.viewport(550, 750) // stuff just somtimes gets outside of the screan
    cy.visit('http://localhost:3000');
    cy.contains('div', 'Email Address').find('input[type=text]').type(email);
    cy.get('form').submit();
    cy.get('.title-overlay').last().click();
    cy.wait(2000);
  });

  // Test case 1: should create a new todo item when a non-empty description is entered and the "Add" button is clicked
  it('Test case 1: should create a new todo item when a non-empty description is entered and the "Add" button is clicked', () => {
    const todoDescription = 'Buy groceries';

    // add a new todo item
    cy.get('.inline-form input[type="text"]').type(todoDescription);
    cy.get('.inline-form input[value="Add"]').click();
    
    // check if the todo item is added
    cy.get('.todo-list')
      .find('.todo-item').last()
      .find('.editable')
      .should('have.text', todoDescription);
  });
  // Test case 2: should not create a new todo item when an empty description is entered and the "Add" button is clicked
  it('Test case 2: should not create a new todo item when an empty description is entered and the "Add" button is clicked', () => {
    // Click on the task to open it
    cy.get('.inline-form input[type="text"]').clear({ force: true })
     .get('.inline-form input[value="Add"]').should('be.disabled');
  });

  after( () => {
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
});
