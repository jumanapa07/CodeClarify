# models.py
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone

# seq2seq_model.py

import torch
import torch.nn as nn
from transformers import RobertaConfig, RobertaModel

class Seq2Seq(nn.Module):
    def __init__(self, encoder, decoder, config, beam_size, max_length, sos_id, eos_id):
        super(Seq2Seq, self).__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.config = config
        self.beam_size = beam_size
        self.max_length = max_length
        self.sos_id = sos_id
        self.eos_id = eos_id

    def forward(self, input_ids, decoder_input_ids):
        # Encoding input sequence using the pretrained Roberta encoder
        encoder_outputs = self.encoder(input_ids)

        # Initializing the decoder hidden state
        decoder_hidden_states = encoder_outputs.last_hidden_state

        # Forward pass through the Transformer decoder
        decoder_outputs = self.decoder(
            decoder_input_ids=decoder_input_ids,
            encoder_hidden_states=decoder_hidden_states
        )

        return decoder_outputs.logits

# You can define additional helper functions or customization based on your requirements.

# Example usage:
# config = RobertaConfig.from_pretrained(pretrained_model)
# encoder = RobertaModel.from_pretrained(pretrained_model, config=config)
# decoder_layer = nn.TransformerDecoderLayer(d_model=config.hidden_size, nhead=config.num_attention_heads)
# decoder = nn.TransformerDecoder(decoder_layer, num_layers=6)
# model = Seq2Seq(encoder=encoder, decoder=decoder, config=config,
#                 beam_size=beam_size, max_length=target_length,
#                 sos_id=tokenizer.cls_token_id, eos_id=tokenizer.sep_token_id)

# Save the model
# torch.save(model.state_dict(), 'your_model_path.pth')

class CodeSnippet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    language = models.CharField(max_length=100)
    code = models.TextField(forms.Textarea)
    created_at = models.DateField(auto_now_add=True)
    # tags = models.CharField(max_length=255, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.title
class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    constraint=models.TextField()
    input_format = models.TextField()
    output_format = models.TextField()
    solution = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)

    def __str__(self):
        return self.title
    # def clean(self):
    #     if self.test_cases.count() < 3:
    #         raise ValidationError(_('A problem must have at least 3 test cases.'))

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField()
    expected_output = models.CharField(max_length=255)

    def __str__(self):
        return f"Test case for {self.problem.title}"
    # def clean(self):
    #     # Ensure that there are exactly three test cases associated with the problem
    #     if self.problem.test_cases.count() >= 3:
    #         raise ValidationError('A problem can have at most 3 test cases.')

    # def save(self, *args, **kwargs):
    #     # Ensure that there are exactly three test cases associated with the problem
    #     if self.problem.test_cases.count() >= 3:
    #         raise ValidationError('A problem can have at most 3 test cases.')
    #     super().save(*args, **kwargs)
class Submission(models.Model):
    ACCEPTED = 'Accepted'
    WRONG_ANSWER = 'Wrong Answer'
    COMPILE_ERROR = 'Compile Error'

    STATUS_CHOICES = [
        (ACCEPTED, 'Accepted'),
        (WRONG_ANSWER, 'Wrong Answer'),
        (COMPILE_ERROR, 'Compile Error')
    ]
    challenge = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=100)


    