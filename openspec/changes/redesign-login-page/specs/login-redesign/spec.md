## ADDED Requirements

### Requirement: Glassmorphism Login Card
The login card must use pure CSS glassmorphism without relying on Ant Design's Card component.

#### Scenario: Card Rendering
- **WHEN** the login page renders
- **THEN** the card must have a transparent background (`rgba(255,255,255,0.05)`)
- **THEN** the card must have `backdrop-filter: blur(20px)` applied
- **THEN** the card must have a subtle white border (`rgba(255,255,255,0.1)`)
- **THEN** Ant Design's Card component must NOT be used

### Requirement: Animated Background
The background must feature animated gradient blobs.

#### Scenario: Blob Animation
- **WHEN** the login page loads
- **THEN** three colored blobs (indigo, cyan, violet) must be visible
- **THEN** the blobs must animate with a slow, organic motion (`@keyframes blob`)

### Requirement: Premium Input Styling
Input fields must look dark and transparent, not default white antd inputs.

#### Scenario: Input Appearance
- **WHEN** the email/password inputs render
- **THEN** they must have dark transparent backgrounds
- **THEN** text color must be white
- **THEN** placeholder text must be semi-transparent white
- **THEN** focus state must show a cyan border glow

### Requirement: Gradient Button
The login button must use a gradient instead of a flat color.

#### Scenario: Button Appearance
- **WHEN** the login button renders
- **THEN** it must use an indigo-to-violet gradient background
- **THEN** it must have a hover scale effect
- **THEN** it must have a shadow glow matching the gradient
