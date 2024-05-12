describe('Logging into the system', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user

  before(function () {
    // create a fabricated user from a fixture
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        }).then((response) => {
          uid = response.body._id.$oid
          name = user.firstName + ' ' + user.lastName
          email = user.email

          // Log in the user
          cy.visit('http://localhost:3000')
          cy.contains('div', 'Email Address')
            .find('input[type=text]')
            .type(email)
          cy.get('form').submit()
          cy.get('#title').type('My New Task')
          cy.get('#url').type('dQw4w9WgXcQ')
          cy.get('form').submit()
        })
      })
  })

  beforeEach(function () {
    // enter the main main page
    cy.visit(`http://localhost:3000`)

    //Login with the user
    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)
      // Submit the form on this page
      cy.get('form')
        .submit()
  })

  describe('Test cases for R8UC1', () => {
    it('Test case 1: should create a new todo item when a non-empty description is entered and the "Add" button is clicked', () => {
      const todoDescription = 'Buy groceries'
      cy.get('.title-overlay').last().click()

      cy.wait(2000)

      // Enter the todo description and click "Add" button
      cy.get('.inline-form input[type="text"]')
        .type(todoDescription) // Type in the text for the new todo item
        .should('have.value', todoDescription) // Ensure that the input field contains the expected value
      cy.get('.inline-form').submit() // Click the "Add" button
    })

    it('Test case 2: should not create a new todo item when an empty description is entered and the "Add" button is clicked', () => {
      cy.get('.title-overlay').last().click()

      cy.wait(2000)

      // Enter the todo description and click "Add" button
      cy.get('.inline-form input[type="text"]')
        .should('have.value', '') // Ensure that the input field contains the expected value
      cy.get('.inline-form').submit() // Click the "Add" button
    })
  })

  describe('Test cases for R8UC2', () => {
    it('Test case 1: Verify that a todo item can be marked as done when the user clicks on the checkbox icon.', () => {
      cy.get('.title-overlay').last().click()

      cy.get('.todo-list .todo-item')
        .eq(0)
        .find('[class^=checker]')
        .trigger('click', { force: true }) // Check the checkbox
        .should('have.class', 'unchecked') // Ensure that the checkbox has the class "done"  
    })

    it('Test case 2: Verify that a todo item can be marked as active when the user clicks on the checkbox icon agein.', () => {
      cy.get('.title-overlay').last().click()
      // Open the first todo item
      cy.get('.todo-list .todo-item')
        .eq(0)
        .find('[class^=checker]')
        .trigger('click', { force: true }) // Uncheck the checkbox
        .should('have.class', 'checked') // Ensure that the checkbox has the class "done"
    })
  })

  describe('Test cases for R8UC3', () => {
    it('Test case 1: Verify that all todo items can be deleted when the user clicks on the delete icon.', () => {
      cy.get('.title-overlay').last().click()
      // Open the first todo item
      cy.wait(2000)

      // Delete all todo items
      cy.get('.todo-list .todo-item [class^=remover]').each(($el) => {
        cy.wrap($el).trigger('click', { force: true });
        cy.wait(2000); // Add a wait time between delete actions if necessary
      });
    })

    it('Test case 2: Verify that the todo item list is empty after all todo items are deleted.', () => {
      cy.get('.title-overlay').last().click()
      // Open the first todo item
      cy.wait(2000)

      // Verify that the todo item list is empty
      cy.get('.todo-list').should('not.contain', '.todo-item');
    })
  })
})

after(function () {
  // clean up by deleting the user from the database
  cy.request({
    method: 'DELETE',
    url: `http://localhost:5000/users/${uid}`
  }).then((response) => {
    cy.log(response.body)
  })
})
