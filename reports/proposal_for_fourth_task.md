# Attack Plan

To evaluate the robustness of our German-to-English speech translation model we design adversarial attacks based on selected attributes from the CommonVoice dataset. These attributes include demographic (gender and age) and linguistic (accent) factors.

---

**Rationale for Attribute Selection**:

1. **Accent (Austria, Germany, Switzerland)**:  
   - The model’s performance is likely influenced by variations in accent, as speech translation systems often struggle with subtle pronunciation differences.
   - These accents represent regional diversity within German-speaking populations and are sufficiently represented in our dataset. The abundance of data allows for comprehensive testing without the risk of under-sampling bias.

2. **Gender (Male and Female)**:  
   - Gender-based differences in pitch, speaking style, and vocal characteristics can impact speech recognition and translation accuracy.
   - Including gender in adversarial testing ensures the model is robust across diverse speaker profiles.

3. **Age (Teens, Twenties, Thirties, Fifties, and beyond)**:  
   - Age influences vocal tone and articulation, introducing variability that could affect model performance.
   - The dataset contains diverse age groups, allowing us to test whether the model performs consistently across speakers with age-related variations in speech.

---

**Benefits of Attribute-Based Adversarial Testing**:

- **Real-World Applicability**: Testing the model with realistic variations ensures robustness in real-world applications, where users have diverse accents, genders, and ages.
- **Insight into Biases**: Attribute-based testing helps identify potential biases (e.g., favoring male voices or standard German accent), guiding improvements in training data and model architecture.
- **Fairness and Inclusivity**: Evaluating performance across demographic and linguistic attributes promotes inclusivity by ensuring equitable performance for all user groups.

#### Male Distribution:
| age       |   germany |   austria |   switzerland |
|:----------|----------:|----------:|--------------:|
| fifties   |     28667 |       746 |          2898 |
| fourties  |     56807 |      1067 |           144 |
| seventies |       318 |        25 |            16 |
| sixties   |      5507 |         9 |            36 |
| teens     |     10413 |       257 |           154 |
| thirties  |     51671 |      2705 |           396 |
| twenties  |     71188 |      2023 |           684 |

#### Female Distribution:
| age       |   germany |   austria |   switzerland |
|:----------|----------:|----------:|--------------:|
| eighties  |         4 |         0 |             0 |
| fifties   |      4000 |        82 |           229 |
| fourties  |      2385 |        18 |             0 |
| seventies |        71 |        21 |             0 |
| sixties   |      1351 |         0 |            36 |
| teens     |       147 |        22 |             4 |
| thirties  |      2610 |       352 |             0 |
| twenties  |      5962 |        30 |             5 |