describe('Test cases for R8UC1', () => {
  // Variables to store user information
  let uid;
  let email;
  let task_id;
  let todo_id;
  // Before hook to create a user and login before each test
  before(function() {
    cy.viewport(550, 750) // stuff just somtimes gets outside of the screan
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
    cy.visit('http://localhost:3000');
    cy.contains('div', 'Email Address').find('input[type=text]').type(email);
    cy.get('form').submit();
    cy.get('.title-overlay').last().click();
    cy.wait(2000);
  });

  // Test case 1: Verify that all todo items can be deleted when the user clicks on the delete icon
  it('Test case 1: Verify that all todo items can be deleted when the user clicks on the delete icon', () => {
    /* 
    I had issue with the list of todos not updating so i close the window, reopen it
    then i check if the list of todos is emty. The task is initiated with 1 todo item.
    */
    cy.get('.todo-list .todo-item [class^=remover]').eq(0).click();
    cy.get(".popup .popup-inner button").click();
    cy.get('.title-overlay').last().click();
    //backtrack
    cy.get('.popup .popup-inner button').click();
    cy.get('.title-overlay').last().click();
    cy.wait(2000);
    cy.get('.todo-list .todo-item').should('have.length', 1);

  });

  after(() => {
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
});
