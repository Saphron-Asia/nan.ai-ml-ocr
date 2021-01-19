# How to collaborate

Hi there! We're thrilled that you'd like to contribute to this project. Your help is essential for keeping it great.
Contributions to this project are released to the public under the project's open source license [link to license].
Please note that this project is released with a Contributor Code of Conduct [link to C.o.C]. By participating in this project you agree to abide by its terms.

## We Develop with Github
We use github to host code, to track issues and feature requests, as well as accept pull requests.

## Reporting a bug
This section guides you through submitting a bug report. Following these guidelines helps maintainers and the community understand your report 📝, reproduce the behavior 💻 💻, and find related reports 🔎.
Before submitting a bug report, make sure that your issue isn’t already filed: [link to github issues page]
Bugs are tracked as GitHub issues. Create an issue and fill up this template: 

```
Description:

Steps to Reproduce:
1.
2.
3.

Expected behavior:

Actual behavior:

Reproduces how often:

Versions:

Additional information:
```

* Write bug reports with detail, background, and sample code. This ensures that the maintainers would be able to reproduce the issue in the shortest possible time. A good bug report should:

  * Use a clear and descriptive title

  * Be very specific in describing the steps in reproducing the problem and provide examples if possible

  * Describe the erratic behavior 

  * Explain which behavior you expected to see instead and why

## Submitting a pull request

1. Fork and clone the repository
2. Configure and install the dependencies
3. Make sure the tests pass on your machine (if applicable)
4. Create a new branch: git checkout -b my-branch-name
5. Make your change, add tests, and make sure the tests still pass.
6. Push to your fork and submit a pull request
6. Pat yourself on the back and wait for your pull request to be reviewed and merged.

Here are a few things you can do that will increase the likelihood of your pull request being accepted:
* Follow the style guide.
* Write tests.
* Keep your change as focused as possible. If there are multiple changes you would like to make that are not dependent upon each other, consider submitting them as separate pull requests.
* Write a good commit message.

## Suggesting Enhancements

We welcome improvements to the analytic model that creates predictions for NAN.ai. We may adopt a pull request that sufficiently improves the accuracy and prediction, thus, allowing you to contribute. 

If your pull request is to improve the model, please consider the following steps when submitting a pull request:
* Make sure you are using the latest version of the source code
* Identify how your model is improving prior results
* Run a test using the benchmark data [link to instructions on pulling data from *s3*] provided
* Create a pull request which describes those improvements in the description.
* Work with the data science team to reproduce those results

## Downloading benchmark data

The shell script /script/setup will automatically download these files into the /resources/data directory. Here are the links to the relevant files for visibility:
The s3 links follow this pattern:

```
Add instruction to download from S3
```

The size of the dataset is approximately 20 GB. The various files and the directory structure are explained here [link to data description].
