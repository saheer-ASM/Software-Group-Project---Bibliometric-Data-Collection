# React Login/Signup Form

A beautiful, animated login and signup form built with React. Features a smooth sliding animation that transitions between login and registration forms.

## Features

- ✨ Smooth sliding animations
- 📱 Fully responsive design
- 🎨 Modern UI with Poppins font
- 🔐 Separate login and registration forms
- 🌐 Social login buttons (Google, Facebook, GitHub, LinkedIn)
- 💅 Clean and maintainable code structure

## Project Structure

```
react-auth-form/
├── public/
│   └── index.html
├── src/
│   ├── AuthForm.jsx      # Main authentication component
│   ├── AuthForm.css      # Component styles
│   ├── App.js            # Root component
│   ├── App.css           # App styles
│   ├── index.js          # React entry point
│   └── index.css         # Global styles
├── package.json
└── README.md
```

## Installation

1. Make sure you have Node.js installed (v14 or higher)

2. Install dependencies:
```bash
npm install
```

## Running the Application

Start the development server:
```bash
npm start
```

The app will open at [http://localhost:3000](http://localhost:3000)

## Usage

The component is simple to use:

```jsx
import AuthForm from './AuthForm';

function App() {
  return (
    <div className="App">
      <AuthForm />
    </div>
  );
}
```

## Customization

### Colors
Edit the CSS variables in `AuthForm.css`:
- Primary color: `#7494ec` (buttons and sliding panel)
- Background gradient: `linear-gradient(90deg, #e2e2e2, #c9d6ff)`

### Form Submission
Add your authentication logic in the `handleLoginSubmit` and `handleRegisterSubmit` functions in `AuthForm.jsx`.

### Social Login
Update the social login links in the component to integrate with your authentication providers.

## Build for Production

Create an optimized production build:
```bash
npm run build
```

The build folder will contain the production-ready files.

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Credits

Original design by @leonam-silva-de-souza
Converted to React component

## License

MIT License - feel free to use this in your projects!
