// API3-001 TRUE POSITIVE: entire req.body bound to model — mass assignment
const express = require('express');
const router = express.Router();

router.put('/users/:id', async (req, res) => {
    const user = await User.findById(req.params.id);
    // Attacker can set isAdmin, role, creditBalance via req.body
    Object.assign(user, req.body);
    await user.save();
    res.json(user);
});
