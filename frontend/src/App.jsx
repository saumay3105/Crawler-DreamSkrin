import { useState } from 'react'

import ContactFinder from './ContactFinder'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <ContactFinder/>
    </>
  )
}

export default App
