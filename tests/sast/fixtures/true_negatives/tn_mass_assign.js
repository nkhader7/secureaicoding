// API3-001 TRUE NEGATIVE: explicit field allowlist used
const express = require('express');
const router = express.Router();

router.put('/users/:id', async (req, res) => {
    const { name, email, bio } = req.body;  // only safe fields extracted
    const user = await User.findByIdAndUpdate(
        req.params.id,
        { name, email, bio },               // never req.body directly
        { new: true, runValidators: true }
    );
    res.json({ id: user.id, name: user.name, email: user.email });
});
