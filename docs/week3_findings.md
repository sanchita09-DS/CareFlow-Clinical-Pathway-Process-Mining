# Week 3 Findings — Clinical Pathway Bottleneck Analysis

## Objective

Quantify the additional time associated with loop-back patient journeys and identify the transition with the largest observed delay.

## Journey Duration Comparison

The analysis identified two patient pathway types:

| Pathway | Patients | Average Duration (min) | Median Duration (min) |
|---|---:|---:|---:|
| Normal | 232 | 75.07 | 76 |
| Loop-back | 68 | 153.81 | 154 |

Loop-back journeys take an average of **78.74 additional minutes** compared with normal journeys.

## Loop-back Pathway

The loop-back pathway follows:

`Registration -> Triage -> Doctor -> X-Ray -> Triage -> Doctor -> Discharge`

The loop-back pattern occurs in **68 of 300 cases (22.67%)**.

## Bottleneck Analysis

The transition with the largest observed average delay is:

**X-Ray -> Triage: 27.1 minutes**

Other observed transition averages include:

- Doctor -> Discharge: 25.6 minutes
- Registration -> Triage: 25.1 minutes
- Triage -> Doctor: 24.8 minutes
- Doctor -> X-Ray: 24.7 minutes

The X-Ray -> Triage transition is therefore the primary bottleneck identified in the observed event data.

This identifies the largest observed transition delay; it does not by itself establish the root cause of that delay.

## Dashboard

The Week 3 Power BI dashboard contains:

1. Extra time due to loop-back
2. Average journey duration by pathway type
3. Patient pathway distribution
4. Top 10 longest patient journeys

The dashboard is connected to the CareFlow BigQuery data and provides a visual summary of the Week 3 analysis.

## Recommendation

A hospital administrator should investigate the handoff and waiting process between **X-Ray and Triage** first, while also examining the broader loop-back pathway to understand why these additional activities occur.

## Week 3 Conclusion

The analysis shows that loop-back journeys are substantially longer than normal journeys, with an average additional duration of **78.74 minutes**. The largest observed transition delay is **X-Ray -> Triage at 27.1 minutes**, making it the first transition to investigate for potential process improvement.
