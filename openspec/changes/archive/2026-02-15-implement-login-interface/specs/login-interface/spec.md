## ADDED Requirements

### Requirement: Immersive Visual Design
The login page must adhere to the "Ethereal Nebula" design system, creating a premium and modern first impression.

#### Scenario: Page Load
- **WHEN** user visits `/login`
- **THEN** display `<BackgroundBlobs />` covering the full viewport with a moving mesh gradient
- **THEN** display the login form in a centered Glass Card container (`.glass-panel`)
- **THEN** animate the card floating up (`y: 20 -> 0`) and fading in (`opacity: 0 -> 1`) using `framer-motion`

### Requirement: Glassmorphism Form Elements
Form inputs must seamlessly integrate with the glass background.

#### Scenario: Input Rendering
- **WHEN** inputs are rendered
- **THEN** they must be semi-transparent with white text
- **THEN** icons (User/Lock) must be `soul-indigo` color
- **THEN** placeholders must be legible against the glass background

### Requirement: Authentication Logic
The form must handle user credentials securely and provide visual feedback.

#### Scenario: Submit Form
- **WHEN** user clicks "Login"
- **THEN** show a loading spinner on the button
- **THEN** call `useAuthStore.getState().login({ email, password })`

#### Scenario: Successful Login
- **WHEN** login API returns success
- **THEN** display a success toast message
- **THEN** redirect user to `/dashboard`

#### Scenario: Failed Login
- **WHEN** login API returns error
- **THEN** display an error toast message with the reason
- **THEN** reset loading state on the button
